import os

from PyQt5 import QtCore, QtGui, QtWidgets

import model.pcap as pcap
from model.report import report
from view.csv2tab import csv2bar


class MainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 592)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)
        main_window.setAutoFillBackground(True)
        main_window.setStyleSheet("")
        main_window.setTabShape(QtWidgets.QTabWidget.Triangular)
        main_window.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(self.open())
        self.actionOpen.setShortcutVisibleInContextMenu(True)
        self.actionOpen.setObjectName("actionOpen")
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
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(filter='pcap')
        name, network, indi = pcap.main(filename)

        report(name, indi, network)
