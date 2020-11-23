#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from os import listdir
from os.path import isfile, join

from PyQt5.QtWidgets import QApplication, QMainWindow

sys.path.append(os.path.dirname(os.getcwd()) + '/model')
import os.path
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from model import pcap
from view.csv2tab import csv2bar
from view.jsonread import json_report
from view.score import score
from view.report import merge_pdfs
from time import perf_counter
import hashlib
import sqlite3
import json
from datetime import datetime

version = 1.0


class First(QMainWindow):

    def __init__(self, parent=None):
        """MainWindow constructor."""
        super(First, self).__init__(parent)
        self.title = 'IHM'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 750
        self.setWindowTitle(self.title)
        image = qtg.QPixmap(os.path.dirname(os.getcwd()) + '/fond.jpg')
        image.scaled(32, 32, qtc.Qt.KeepAspectRatio, qtc.Qt.FastTransformation)
        self.image0 = qtg.QImage(image)
        palette = qtg.QPalette()
        palette.setBrush(qtg.QPalette.Background, qtg.QBrush(image))
        self.setPalette(palette)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Central Widget
        self._main = qtw.QWidget()
        layoutV = qtw.QVBoxLayout()
        layoutV.addWidget(qtw.QLabel(
            '<strong><font size=20  color=\"#00CED1\">Ceci est une interface           graphique permettant d analyser les fichiers PCAP. <br />Ce logiciel a notamment pour but de comparer plusieurs fichiers afin de les trier et <br /> d evaluer  les plus aptes a l entrainement des sondes de detections.<font></strong>'))
        layoutV.addWidget(qtw.QLabel(
            '<strong><font size=20 color=\"#00CED1\">Pour commencer l analyse de fichier veuillez presser le bouton ci dessous  pour parcourir<br/> les fichiers :</font></strong>'))
        Label = qtw.QLabel(self)
        Label.setPixmap(image)
        Label.resize(image.width(), image.height())
        # layoutV.addWidget(Label)
        button = qtw.QPushButton('open')
        layoutV.addWidget(button)
        button.clicked.connect(self.open)

        self._main.setLayout(layoutV)
        self.textedit = qtw.QTextEdit()
        self.setCentralWidget(self._main)
        # Menu Bar
        menu = self.menuBar()  # -> QMenuBar
        file_menu = menu.addMenu('File')  # -> QMenu
        tool_menu = menu.addMenu('Tool')

        # Add keyboard shortcuts using QKeySequence constants
        file_menu.addAction(
            'Open',
            self.open,
            # This uses a platform-appropriate Open shortcut:
            qtg.QKeySequence.Open,
        )
        # ToolBar
        edit_toolbar = self.addToolBar('Edit')
        self.statusBar().showMessage('IHM Analyse de trace réseau')
        self.show()

    def open(self):  # le replace sert aux chemins sur windows

        filename, _ = qtw.QFileDialog.getOpenFileName()
        sha256 = hashlib.sha256(open(filename, 'rb').read()).hexdigest()
        if filename:
            with open(filename, 'r') as handle:
                t1 = perf_counter()
                text = repr(filename).replace('\\', '/')
                text2 = text.replace("'", "")

                # output = pcap.main(text2)

                output = pcap.main([text2])

                if not os.path.exists(output + '/pdf/Resultats.pdf'):  # verifie si le fichier a déjà été analysé

                    if os.path.exists(output + '/csv/flow_matrix.csv'):
                        csv2bar(output + '/csv/flow_matrix.csv')
                    if os.path.exists(output + '/csv/machine_use.csv'):
                        csv2bar(output + '/csv/machine_use.csv')
                    if os.path.exists(output + '/csv/machine_role.csv'):
                        csv2bar(output + '/csv/machine_role.csv')

                    # creation du graph spyder
                    json_report(output + '/indicators.json', output)

                    pdfs = [f for f in os.listdir(output + '/pdf/') if os.path.isfile(f) and f.endswith('.pdf')]
                    merge_pdfs(pdfs, output + '/pdf/')
                S = score(output + '/indicators.json', output + '/result.json')
                with open(output + '/score.txt', 'w') as f:
                    f.write('Le score totale est: ' + str(S[0]) + '/40' + '\n')
                    f.write('La présence des ports à surveiller est: ' + str(S[1]) + '/10' + '\n')
                    f.write('Le score de taille de l architecture est: ' + str(S[2]) + '/10' + '\n')
                    f.write('Le score du ratio nombre IP échange: ' + str(S[3]) + '/10' + '\n')
                    f.write('Le score taux de réponse moyen: ' + str(S[4]) + '/10' + '\n')
                    f.write('La capture réseau est de ' + str(S[5]) + ' secondes' + '\n')

                self.second_m(S)  # ouverture de le seconde fenêtre

                open_file(output + '/pdf/Resultats.pdf')  # ouverture du fichier pdf

                with open(output + '/result.json', "r") as f:
                    content2 = json.load(f)
                    start = content2['start']
                    end = content2['end']
                start_dt = datetime.fromtimestamp(start)
                end_dt = datetime.fromtimestamp(end)

                with open(output + '/indicators.json', "r") as f:
                    content = json.load(f)
                    a = content['exchanges']
                    b = content['ips']
                    c = content['response_avg']
                    d = len(content['ports'])
                    e = content['ip_life']['1st_quartile']
                    f = content['ip_life']['variance']

                t2 = perf_counter()
                # print (t2-t1)

                insert_db(sha256, output, S[0], b, d, c, f, start_dt, end_dt, t2 - t1, version)

    def second_m(self, scr):
        """Lance la deuxième fenêtre"""
        self.second = second(scr)

        self.second.setWindowModality(qtc.Qt.ApplicationModal)

        # appel de la deuxième fenêtre
        self.second.show()


def insert_db(sha256, nom, score, nombre_ip, nombre_port, taux_de_reponse, variance_ip_life, debut_de_capture,
              fin_de_capture, temps_analyse_en_sec, version):
    if not os.path.exists(os.getcwd() + '/resultat.db'):
        conn = sqlite3.connect('resultat.db')
        cur = conn.cursor()

        sql = '''CREATE TABLE analyse (


                        sha256 TEXT PRIMARY KEY NOT NULL,
                        score FLOAT ,
                        nombre_ip INT ,
                        nombre_port INT ,
                        taux_de_reponse FLOAT,
                        variance_ip_life FLOAT
            );'''
        cur.execute(sql)
        conn.commit()
        sql2 = '''CREATE TABLE PCAP (


                    id INTEGER PRIMARY KEY,
                    date_analyse DATE ,
                    version DECIMAL ,
                    nom_PCAP TEXT ,
                    sha256 TEXT,
                    debut_capture DATETIME,
                    fin_capture DATETIME,
                    temps_analyse FLOAT
            );'''

        cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()

    try:
        conn = sqlite3.connect('resultat.db')
        cur = conn.cursor()
        print("Connexion réussie à SQLite")
        sql = "INSERT INTO analyse (sha256, score, nombre_ip, nombre_port, taux_de_reponse, variance_ip_life) VALUES (?, ?, ?, ?, ?, ?)"
        value = (sha256, score, nombre_ip, nombre_port, taux_de_reponse, variance_ip_life)
        cur.execute(sql, value)
        sql3 = "INSERT INTO PCAP (date_analyse, version, nom_PCAP, sha256, debut_capture, fin_capture, temps_analyse) VALUES (?, ?, ?, ?, ?, ?, ?)"
        value2 = (
            str(datetime.now().date()), version, nom, sha256, debut_de_capture, fin_de_capture, temps_analyse_en_sec)
        cur.execute(sql3, value2)
        conn.commit()
        print("Enregistrement inséré avec succès dans la table resultat")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table resultat", error)


class second(qtw.QWidget):  # définition de la 2eme fenetre
    def __init__(self, scr, parent=None):
        super(second, self).__init__(parent)
        self.setWindowTitle(u"Score")
        self.setStyleSheet("QLabel { font: 18pt; }")
        self._main = qtw.QWidget()

        layoutV = qtw.QVBoxLayout()
        layoutV.addWidget(qtw.QLabel('Le score total est'))
        layoutV.addWidget(qtw.QLabel(str(scr[0])))
        layoutV.addWidget(qtw.QLabel('Le score de présence des ports à surveiller est:'))
        layoutV.addWidget(qtw.QLabel(str(scr[1]) + '/10'))
        layoutV.addWidget(qtw.QLabel(' Score de taille de l architecture est:'))
        layoutV.addWidget(qtw.QLabel(str(scr[2]) + '/10'))
        layoutV.addWidget(qtw.QLabel('Le score du ratio nombre ip échange:'))
        layoutV.addWidget(qtw.QLabel(str(scr[3]) + '/10'))
        layoutV.addWidget(qtw.QLabel('Le score taux de réponses moyen:'))
        layoutV.addWidget(qtw.QLabel(str(scr[4]) + '/10'))

        self.setLayout(layoutV)

    def ok_m(self):
        # emettra un signal "fermeturequelclient()" avec l'argument cité
        self.emit(SIGNAL("fermeturequelclient(PyQt_PyObject)"), unicode(self.lineEdit.text()))
        # fermer la fenêtre
        self.close()


def open_file(filename):  # permet à tous les systèmes d'exploitation d'ouvrir les PDF avec l'application par defaut
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

    def search(self, term, case_sensitive=False):
        if case_sensitive:
            cur = self.textedit.find(
                term,
                qtg.QTextDocument.FindCaseSensitively
            )
        else:
            cur = self.textedit.find(term)
        if not cur:
            self.statusBar().showMessage('No matches Found', 2000)

        open.clicked.connect(self.on_pushButton_clicked)
        self.dialog = Second(self)

    def on_pushButton_clicked(self):
        self.dialog.show()


def main():
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    app = QApplication(sys.argv)
    sheet = Sheet()
    sys.exit(app.exec_())
