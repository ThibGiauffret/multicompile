#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MultiCompile v0.5-alpha
Généré le 26 Juillet 2021
@author: Th. G

Ce logiciel est mis à disposition sous licence Creatice Commons 
(Pas d'utilisation commerciale, Partage dans les mêmes conditions).
"""

from PyQt5.QtWidgets import (QFileDialog, QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QScrollBar, QSizePolicy, QTextEdit, QLineEdit, QTableWidget, QTabWidget, QVBoxLayout, QWidget, QTableWidgetItem, QHeaderView,QSplitter,QProgressBar)
from PyQt5.QtCore import QProcess, Qt, QObject, QThread, pyqtSignal,pyqtSlot,QRunnable , QThreadPool
from PyQt5.QtGui import QIcon
from threading import *

import re
from subprocess import call
from subprocess import Popen
import os
import sys
import platform
import traceback
system = platform.system()
if system == "Linux" :
    pass
else :
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from pathlib import Path
from shutil import copyfile
import time


compiler = ""
nonstopmode = ""
jobname = ""
options = ""

if getattr(sys, 'frozen', False):
    application_path = str(Path(os.path.dirname(os.path.realpath(sys.executable))))
elif __file__:
    application_path = str(Path(os.path.dirname(os.path.realpath(__file__))))



class MainWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.running = False

        self.GroupBox = QGroupBox()
        self.GroupBox.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        self.tableWidget = QTableWidget(1, 4)
        self.tableWidget.setProperty('class', 'mytable')

        self.tableWidget.setHorizontalHeaderLabels(["Emplacement", "Nom", "Ouvrir", "Supprimer" ]) 
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        for i in range(rows):
            for j in range(columns):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        GroupBoxLayout = QVBoxLayout()
        GroupBoxLayout.setContentsMargins(0, 0, 0, 0)
        GroupBoxLayout.addWidget(self.tableWidget)
        self.addPushButton = QPushButton("Ajouter un emplacement")
        self.addPushButton.setDefault(True)
        GroupBoxLayout.addWidget(self.addPushButton)
        GroupBoxLayout.addStretch(1)
        self.GroupBox.setLayout(GroupBoxLayout)
        
        
        self.LogBox = QTabWidget()
        
        
        # Initialize tab screen
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        

        self.LogBox.addTab(self.tab1,"Log")
        self.LogBox.addTab(self.tab2,"Paramètres")
        

        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        
        
        
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        log = "<span style=\" font-size:10pt; font-weight:600;\" >Bienvenue dans MultiCompile !</span>\n\n"
        self.textEdit.append(log)
 
        self.tab1.layout.addWidget(self.textEdit)
        
        self.progressLabel = QLabel()
        self.progressBar = QProgressBar()
        self.runPushButton = QPushButton("Compiler !")
        self.runPushButton.setProperty('class', 'success')
        
        h_layout = QHBoxLayout()
        self.tab1.layout.addLayout(h_layout)
        
        h_layout.addWidget(self.progressBar)
        h_layout.addWidget(self.progressLabel)
        h_layout.addWidget(self.runPushButton)

        
        self.tab1.setLayout(self.tab1.layout)

        self.ParamBox = QGroupBox("Paramètres")
        self.compilerLabel = QLabel()
        self.compilerLabel.setText("Compilateur")
        self.compilerComboBox = QComboBox()
        self.compilerComboBox.addItems(["pdflatex","xelatex","lualatex"])
        self.parentLabel = QLabel()
        self.parentLabel.setText("Emplacement par défaut")
        self.parentText = QLineEdit()
        self.parentText.setText(application_path)
        self.savePushButton = QPushButton("Sauvegarder les paramètres")
        self.savePushButton.setDefault(True)
        #logPushButton = QPushButton("Voir le log")
        self.splitter = QSplitter(Qt.Horizontal)

        try :
            f= open(Path(application_path + '/' +  "config.txt"),"r")
            contents = f.readlines()
            var = str(contents[0])
            var2 = str(contents[1])
            #print(var)
            index = self.compilerComboBox.findText(var.strip(), Qt.MatchFixedString)
            print('Configuration chargée !')  
            if index >= 0:
                self.compilerComboBox.setCurrentIndex(index)
                self.parentText.setText(var2)
            f.close()
        except FileNotFoundError:
            print('Pas de fichier config.txt !')
            f= open(Path(application_path + '/' + "config.txt"),"w+")
            contents = ["pdflatex\n",application_path+'\n']
            with open(Path(application_path  + '/' +  "config.txt"), "w") as f:
                f.writelines(contents)
                f.close()

        self.groupCompile = QGroupBox("Compilateur")
        self.vboxCompile = QVBoxLayout()
        #groupCompile.setStyleSheet('background: palette(window);')
        self.vboxCompile.addWidget(self.compilerComboBox)
        self.groupCompile.setLayout(self.vboxCompile)
        self.tab2.layout.addWidget(self.groupCompile)
        
        
        self.groupParent = QGroupBox("Emplacement par défaut")
        self.vboxParent = QVBoxLayout()
        #groupParent.setStyleSheet('background: palette(window);')
        self.vboxParent.addWidget(self.parentText)
        self.groupParent.setLayout(self.vboxParent)
        self.tab2.layout.addWidget(self.groupParent)
        
        self.tab2.layout.addWidget(self.splitter)
        
        self.tab2.layout.addWidget(self.savePushButton)
        
       
        
        #layout.addWidget(logPushButton)
        #tab2.layout.addStretch(1)
        
        
        
        self.tab2.setLayout(self.tab2.layout)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.GroupBox, 0, 0)
        self.mainLayout.addWidget(self.LogBox, 1, 0)
        #mainLayout.addWidget(ParamBox, 2, 1)
        
                
        self.setLayout(self.mainLayout)

        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("MultiCompile")

        self.addPushButton.clicked.connect(self.add_path)
        self.runPushButton.clicked.connect(self.run)
        #self.runPushButton.clicked.connect(self.start_in_thread)
        self.savePushButton.clicked.connect(self.save_param)

    def refresh_textedit(self,MYSTRING,color): 
        if color == "red":
            redText = "<span style=\" font-size:8pt; font-weight:400; color:#ff0000;\" >"+MYSTRING+"</span>"
            self.textEdit.append(redText)
        elif color == "green":
            greenText = "<span style=\" font-size:8pt; font-weight:400; color:#2bbe00;\" >"+MYSTRING+"</span>"
            self.textEdit.append(greenText)
        elif color == "greenbold":
            greenText = "<span style=\" font-size:8pt; font-weight:600; color:#2bbe00;\" >"+MYSTRING+"</span>"
            self.textEdit.append(greenText)
        elif color == "gray":
            greenText = "<span style=\" font-size:8pt; font-weight:400; color:#535353;\" >"+MYSTRING+"</span>"
            self.textEdit.append(greenText)
        elif color == "blue":
            greenText = "<span style=\" font-size:8pt; font-weight:400; color:#3ca0ff;\" >"+MYSTRING+"</span>"
            self.textEdit.append(greenText)
        else :
            self.textEdit.append( "<span style=\" font-size:8pt; font-weight:400;\" >"+MYSTRING+"</span>") #append string
        QApplication.processEvents() #update gui for pyqt


    def run(self) :

        self.runPushButton.setProperty('class', 'danger')
        self.runPushButton.setText("En cours...")
        self.runPushButton.setEnabled(False)

        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progress_counter = 0


        self.running = True
    
        self.LogBox.setCurrentWidget(self.tab1)
        
        rowPosition = self.tableWidget.rowCount()

        self.emplacement_counter = 1
        self.nbEmplacements = rowPosition-1
        log = str(rowPosition-1) + ' emplacement(s) chargé(s). Les documents seront disponibles dans un sous-dossier output.'
        self.refresh_textedit(log, "black")
        for path in range(0, rowPosition-1, 1) :
            self.init_path = str(self.tableWidget.item(path, 0).text())
            self.refresh_textedit('<br><span style=\" font-size9pt; font-weight:600;\" >--> ' + str(os.path.basename(os.path.normpath(self.init_path))) + '</span>', "black")
            
            self.chapter = os.path.basename(os.path.normpath(self.init_path))
            
            subdir = os.listdir(self.init_path)
            #print(subdir)
            folders = []
            
            for g in subdir :
                if g.find('.') != -1 :
                    pass
                else :
                    folders.append(g)
                
            self.refresh_textedit('Les sous-dossiers sont : ' + str(folders) + '.', "black")

            self.counter_folder = 0
            self.total_folders=0

            self.progressBar.setFormat('Compilation de '+str(self.chapter)+' : 0%')

            if os.path.exists(Path(self.init_path + '/master.tex')):
                self.mypath = os.path.normpath(self.init_path)
                self.folder = str(os.path.basename(os.path.normpath(self.mypath)))
                os.chdir(self.mypath)
                self.compile()
                
            for k in folders :
                path = self.init_path + k
                
                path = os.path.normpath(path)
                #print(path)
                os.chdir(path)
            
                if os.path.exists(path + '/master.tex'):
                    self.total_folders+=1
        
            for h in folders :
                self.folder = h
                self.mypath = self.init_path + h
                
                self.mypath = os.path.normpath(self.mypath)
                #print(path)
                os.chdir(self.mypath)
            
                if os.path.exists(self.mypath + '/master.tex'):
                    self.counter_folder+=1
                    self.compile()
                    
                else :
                    self.refresh_textedit('Pas de fichier \"master.tex\" trouvé dans ' + str(h) + '...', "blue")

        self.progressBar.setFormat('Compilations terminées !')

        self.progressBar.setValue(100)

        self.LogBox.setTabEnabled(1,True) 

        self.runPushButton.setProperty('class', 'success')
        self.runPushButton.setText("Compiler !")
        self.runPushButton.setEnabled(True)

    
  
    def start_in_thread(self):
        t1=Thread(target=self.run)
        if self.running == True :
            t1.stop()
            self.runPushButton.setText("Compiler !")
            self.runPushButton.setProperty('class', 'success')
            self.running = False
            self.refresh_textedit('Processus de compilation avorté !', "red")
        else:
            t1.start()
        

    def compile(self):

        error = 0
        f = open(Path(self.mypath + "/master.tex"),"r")
        print(f)
        contents = f.readlines()
        c = 0
        self.audiences = []
        for i in range (0,len(contents),1) :
            line = str(contents[i])
            check = line.find("SetNewAudience")
            if check == -1 :
                c += 1
            else :
                m = re.search(r"\{([A-Za-z0-9_]+)\}", contents[i])
                self.audiences.append(m.group(1))
                c += 1
        if self.audiences == [] :

            call('cd ' + self.mypath, shell=True)
            nonstopmode = '-halt-on-error'
            jobname = '-jobname=' + self.chapter + '_' + self.folder + '-master'
            options = '"\input{master}"'
            compiler = str(self.compilerComboBox.currentText())
            
            self.command = [compiler, nonstopmode, jobname, options]

            result = call(self.command)
            
            error=0

            if result == 0 :
                try:
                    os.mkdir(Path(self.init_path + '/output'))
                except FileExistsError:
                    pass
                try:
                    copyfile(Path(self.mypath + '/' + self.chapter + '_' + self.folder + '-master'  + '.pdf') , Path(self.init_path + 'output/' + self.chapter + '_' + self.folder + '-master' + '.pdf'))
                except FileNotFoundError:
                    self.refresh_textedit('Une erreur est survenue lors de la copie du pdf...', "red")
                    error+=1
            else :
                self.refresh_textedit("No success ?", "black")
                error+=1
                pass
            
            if error == 0:
                self.refresh_textedit('Compilation du document ' + self.folder + '" terminée avec ' + str(error) + ' erreur(s).', "greenbold")
            else:
                self.refresh_textedit('Compilation du document ' + self.folder + '" terminée avec ' + str(error) + ' erreur(s).', "red")
                self.refresh_textedit("Fichier log disponible ici : "+str(Path(self.mypath + '/' + self.chapter + '_' + self.folder + '-master' + '.log')), "red")

        else :
            self.refresh_textedit('Les audiences trouvées dans "' + self.folder + '" sont : ' + str(self.audiences) + '. Compilation en cours...', "black")

            self.counter=1
            self.percentage=0

            
            for j in self.audiences :

                if self.total_folders != 0:
                    self.percentage+=int((1/self.total_folders)*(1/len(self.audiences))*100)
                    
                    self.progressBar.setFormat('Compilation de '+str(self.chapter)+' : '+str(self.percentage)+'%')
                else :
                    self.percentage+=int((1/len(self.audiences))*100)
                    
                    self.progressBar.setFormat('Compilation de '+str(self.chapter)+' : '+str(self.percentage)+'%')

                
                self.audience = j
                
                call('cd ' + self.mypath, shell=True)
                nonstopmode = '-halt-on-error'
                jobname = '-jobname=' + self.chapter + '_' + self.folder + '-' + j
                options = '"\def\ismulticompile{1}\def\CurrentAudience{' + self.audience + '}\input{master}"'
                compiler = str(self.compilerComboBox.currentText())
                
                self.command = [compiler, nonstopmode, jobname, options]

                result = call(self.command)
                
                error=0

                if result == 0 :
                    try:
                        os.mkdir(Path(self.init_path + '/output'))
                    except FileExistsError:
                        pass
                    try:
                        copyfile(Path(self.mypath + '/' + self.chapter + '_' + self.folder + '-' + self.audience + '.pdf') , Path(self.init_path + 'output/' + self.chapter + '_' + self.folder + '-' + self.audience + '.pdf'))
                    except FileNotFoundError:
                        self.refresh_textedit('Une erreur est survenue lors de la copie du pdf...', "red")
                        error+=1
                else :
                    self.refresh_textedit("No success ?", "black")
                    error+=1
                    pass
                
                if error == 0:
                    self.refresh_textedit('Compilation de l\'audience '+ self.audience + ' de "' + self.folder + '" terminée avec ' + str(error) + ' erreur(s).', "greenbold")
                else:
                    self.refresh_textedit('Compilation de l\'audience '+ self.audience + ' de "' + self.folder + '" terminée avec ' + str(error) + ' erreur(s).', "red")
                    self.refresh_textedit("Fichier log disponible ici : "+str(Path(self.mypath + '/' + self.chapter + '_' + self.folder + '-' + self.audience + '.log')), "red")

                self.counter+=1

                

                #Pb de threading ici...

                if self.total_folders != 0:
                    self.progress_counter+=int((1/self.nbEmplacements)*(1/self.total_folders)*(1/len(self.audiences))*100)
                    
                    self.progressBar.setValue(self.progress_counter)
                else:
                    self.progress_counter+=int((1/self.nbEmplacements)*(1/len(self.audiences))*100)
                    
                    self.progressBar.setValue(self.progress_counter)
                
                #os.system('xdg-open ' + name + '-' + j + '.pdf > /dev/null')
            
            
            #LogBox.setCurrentWidget(tab1)


    def add_path(self) :
        file = str(QFileDialog.getExistingDirectory(self, "Selectionner un dossier",str(self.parentText.text())))
        rowPosition = self.tableWidget.rowCount()
        self.item = QTableWidgetItem()
        self.item.setText(file+'/')
        self.tableWidget.setItem(rowPosition-1, 0, self.item)
        self.chapters = QTableWidgetItem()
        self.chapters.setText(os.path.basename(os.path.normpath(file)))
        self.tableWidget.setItem(rowPosition-1, 1, self.chapters)
        self.viewPushButton = QPushButton(self.tableWidget)
        self.viewPushButton.setText('Ouvrir')
        self.tableWidget.setCellWidget(rowPosition-1, 2, self.viewPushButton)
        self.rmPushButton = QPushButton(self.tableWidget)
        self.rmPushButton.setText('Supprimer')
        self.tableWidget.setCellWidget(rowPosition-1, 3, self.rmPushButton)
        self.tableWidget.insertRow(rowPosition)
        self.rmPushButton.clicked.connect(self.rm_path)
        self.viewPushButton.clicked.connect(self.open_path)
    
    def open_path(self) :
        button = QApplication.focusWidget()
        index = self.tableWidget.indexAt(button.pos())
        location = str(self.tableWidget.item(index.row(), 0).text())
        system = platform.system()
        if system == "Linux" :
            os.system('xdg-open "%s"' % location)
        else :
            os.startfile(location)

    def rm_path(self) :
        button = QApplication.focusWidget()
        index = self.tableWidget.indexAt(button.pos())
        self.tableWidget.removeRow(index.row())
        
    def save_param(self) :
        save_path = application_path + "/config.txt"
        f2= open(save_path,"r+")
        contents = f2.readlines()
        compiler = str(self.compilerComboBox.currentText())
        contents[0] =  compiler + "\n"
        contents[1] =  str(self.parentText.text()) + "\n"

        with open(save_path, "w") as f2:
            f2.writelines(contents)
            f2.close()
        print('Configuration sauvegardée !')
        
    


app = QApplication(sys.argv)

w = MainWindow()

# setup stylesheet
#apply_stylesheet(app, theme='dark_blue.xml')

# stylesheet = app.styleSheet()

# with open('custom.css') as file:
#     app.setStyleSheet(stylesheet + file.read().format(**os.environ))
w.show()



app.exec_()
