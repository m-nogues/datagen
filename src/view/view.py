import os
import sys

import matplotlib

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from view.csv2tab import csv2bar
from model import pcap
from model.report import report

matplotlib.use('Qt5Agg')


# class MplCanvas(FigureCanvas):
#     def __init__(self, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 592)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)
        main_window.setAutoFillBackground(True)
        main_window.setUnifiedTitleAndToolBarOnMac(True)

        # Main window content
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.centralwidget)

        main_window.setCentralWidget(self.scroll)

        # Menu bar
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        main_window.setMenuBar(self.menubar)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        # Open file
        self.actionOpen = QtWidgets.QAction()
        self.actionOpen.setShortcutVisibleInContextMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.open)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Datagen"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

    def open(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(filter='*.pcap*')

        if filename:
            name, network, indi = pcap.main(filename)

            if self.centralwidget.layout():
                QObjectCleanupHandler().add(self.centralwidget.layout())
            layout = QVBoxLayout(self.centralwidget)

            if not os.path.exists(name + '/pdf/results.pdf'):
                if os.path.exists(name + '/csv/flow_matrix.csv'):
                    sc = FigureCanvas(csv2bar(name + '/csv/flow_matrix.csv'))
                    layout.addWidget(sc)
                    sc.draw()
                if os.path.exists(name + '/csv/machine_use.csv'):
                    sc = FigureCanvas(csv2bar(name + '/csv/machine_use.csv'))
                    layout.addWidget(sc)
                    sc.draw()
                if os.path.exists(name + '/csv/machine_role.csv'):
                    sc = FigureCanvas(csv2bar(name + '/csv/machine_role.csv'))
                    layout.addWidget(sc)
                    sc.draw()

            sc = FigureCanvas(report(name, indi))
            layout.addWidget(sc)
            sc.draw()


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.setup_ui(main)
    main.show()

    sys.exit(app.exec_())
