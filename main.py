#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 15:29:10 2019

@author: thibault
"""

import re
from subprocess import call
import os
from shutil import copyfile
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog, QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, 
                             QHBoxLayout, QLabel, QPushButton, QScrollBar, QSizePolicy, QTextEdit,
                             QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem, QHeaderView)


class main(QDialog):
    
   
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        
        GroupBox = QGroupBox("Emplacements")
        GroupBox.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)
        
        def createtable(self):
            tableWidget.setHorizontalHeaderLabels(["Emplacement", "Nom", "Autre"]) 
            rows = tableWidget.rowCount()
            columns = tableWidget.columnCount()
            for i in range(rows):
                for j in range(columns):
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled)
                    tableWidget.setItem(i, j, item)

        tableWidget = QTableWidget(1, 3)
        createtable(self)
        header = tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        GroupBoxLayout = QVBoxLayout()
        GroupBoxLayout.setContentsMargins(5, 5, 5, 5)
        GroupBoxLayout.addWidget(tableWidget)
        addPushButton = QPushButton("Ajouter un emplacement")
        addPushButton.setDefault(True)
        GroupBoxLayout.addWidget(addPushButton)
        rmPushButton = QPushButton("Supprimer l'emplacement sélectionné")
        rmPushButton.setDefault(True)
        GroupBoxLayout.addWidget(rmPushButton)
        GroupBoxLayout.addStretch(1)
        GroupBox.setLayout(GroupBoxLayout)
        
        
        LogBox = QGroupBox("Log")
        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        log = "Bienvenue dans MultiCompile !\n"
        textEdit.setPlainText(log)
        LogBoxLayout = QHBoxLayout()
        LogBoxLayout.setContentsMargins(5, 5, 5, 5)
        LogBoxLayout.addWidget(textEdit)
        LogBox.setLayout(LogBoxLayout)
        
                
        ParamBox = QGroupBox("Paramètres")
        compilerComboBox = QComboBox()
        compilerComboBox.addItems(["pdflatex","xelatex"])
        savePushButton = QPushButton("Sauvegarder")
        savePushButton.setDefault(True)
        #logPushButton = QPushButton("Voir le log")
        runPushButton = QPushButton("Compiler !")
        runPushButton.setStyleSheet("background-color: green; color: white")
        
        try :
            f= open("config.txt","r")
            contents = f.readlines()
            var = str(contents[0])
            #var2 = contents[1]
            #print(var)
            index = compilerComboBox.findText(var.strip(), Qt.MatchFixedString)
            print('Configuration chargée !')  
            if index >= 0:
                compilerComboBox.setCurrentIndex(index)
            f.close()
        except FileNotFoundError:
            print('Pas de fichier config.txt !')
            f= open("config.txt","w+")
            contents = ["pdflatex"]
            with open("config.txt", "w") as f:
                f.writelines(contents)
                f.close()
        
        layout = QVBoxLayout()
        layout.addWidget(compilerComboBox)
        layout.addWidget(savePushButton)
        #layout.addWidget(logPushButton)
        layout.addWidget(runPushButton)
        layout.addStretch(1)
        
        ParamBox.setLayout(layout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(GroupBox, 1, 0, 1, 2)
        mainLayout.addWidget(LogBox, 2, 0)
        mainLayout.addWidget(ParamBox, 2, 1)
        
                
        self.setLayout(mainLayout)

        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("MultiCompile")
        
        def run() :
            
            def refresh_textedit(MYSTRING): 
                textEdit.append(str(MYSTRING)) #append string
                QApplication.processEvents() #update gui for pyqt
        
            rowPosition = tableWidget.rowCount()
            log = str(rowPosition-1) + ' emplacement(s) chargé(s). Les documents seront disponibles dans un sous-dossier output.'
            refresh_textedit(log)
            for path in range(0, rowPosition-1, 1) :
                init_path = str(tableWidget.item(path, 0).text())
                #init_path = r'/home/thibault/MEGAsync/LaTeX/test_cours/'
                refresh_textedit('--> ' + str(init_path))
                
                chapter = os.path.basename(os.path.normpath(init_path))
                
                subdir = os.listdir(init_path)
                #print(subdir)
                folders = []
                
                for g in subdir :
                    if g.find('.') != -1 :
                        pass
                    else :
                        folders.append(g)
                    
                refresh_textedit('Les sous-dossiers sont : ' + str(folders) + '.')
                
                def compile(mypath, h):
                    error = 0
                    f = open(mypath + "/master.tex","r")
                    print(f)
                    contents = f.readlines()
                    c = 0
                    audiences = []
                    for i in range (0,len(contents),1) :
                        line = str(contents[i])
                        check = line.find("SetNewAudience")
                        if check == -1 :
                            c += 1
                        else :
                            m = re.search(r"\{([A-Za-z0-9_]+)\}", contents[i])
                            audiences.append(m.group(1))
                            c += 1
                    if audiences == [] :
                        refresh_textedit('Pas d\'audience trouvée dans "' + h + '"... La compilation simple du fichier tex va être lancée !')
                        call('cd ' + path, shell=True)
                        jobname = '-jobname=' + chapter + '_' + h + '-' + 'master'
                        options = '"\input{master}"'
                        compiler = str(compilerComboBox.currentText())
                        call([compiler, jobname, options])
                        try:
                            os.mkdir(init_path + '/output')
                        except FileExistsError:
                            error+=1
                        copyfile(mypath + '/' + chapter + '_' + h + '-' + 'master' + '.pdf' ,init_path + 'output/' + chapter + '_' + h + '-' + 'master' + '.pdf')
                    else :
                        refresh_textedit('Les audiences trouvées dans "' + h + '" sont : ' + str(audiences) + '.')
                        refresh_textedit(str(len(audiences)) + ' documents pdf seront créés !')
                        
                        for j in audiences :
                            call('cd ' + mypath, shell=True)
                            jobname = '-jobname=' + chapter + '_' + h + '-' + j
                            options = '"\def\CurrentAudience{' + j + '}\input{master}"'
                            compiler = str(compilerComboBox.currentText())
                            call([compiler, jobname, options])
                            try:
                                os.mkdir(init_path + '/output')
                            except FileExistsError:
                                pass
                            try:
                                copyfile(mypath + '/' + chapter + '_' + h + '-' + j + '.pdf' ,init_path + 'output/' + chapter + '_' + h + '-' + j + '.pdf')
                            except FileNotFoundError:
                                refresh_textedit('Une erreur est survenue lors de la copie du pdf...')
                                error+=1
                            #os.system('xdg-open ' + name + '-' + j + '.pdf > /dev/null')
                            
                        refresh_textedit('Compilation de "' + h + '" terminée avec ' + str(error) + ' erreur(s).')
                
                if os.path.exists(init_path + '/master.tex'):
                    newpath = os.path.normpath(init_path)
                    h = str(os.path.basename(os.path.normpath(newpath)))
                    os.chdir(newpath)
                    compile(newpath, h)
                
                for h in folders :
                    path = init_path + h
                    
                    path = os.path.normpath(path)
                    #print(path)
                    os.chdir(path)
                
                    if os.path.exists(path + '/master.tex'):
                        compile(path, h)
                        
                    else :
                        refresh_textedit('Pas de fichier \"master.tex\" trouvé dans ' + str(h) + '...')
                    
        def add_path() :
            file = str(QFileDialog.getExistingDirectory(self, "Selectionner un dossier"))
            rowPosition = tableWidget.rowCount()
            item = QTableWidgetItem()
            item.setText(file+'/')
            tableWidget.setItem(rowPosition-1, 0, item)
            chapter = QTableWidgetItem()
            chapter.setText(os.path.basename(os.path.normpath(file)))
            tableWidget.setItem(rowPosition-1, 1, chapter)
            tableWidget.insertRow(rowPosition)

        def rm_path(self) :
            selected = tableWidget.currentRow()
            tableWidget.removeRow(selected)
            
        def save_param() :
            save_path = os.path.dirname(os.path.realpath(__file__)) + "/config.txt"
            f2= open(save_path,"r+")
            contents = f2.readlines()
            compiler = str(compilerComboBox.currentText())
            contents[0] =  compiler + "\n"
    
            with open(save_path, "w") as f2:
                f2.writelines(contents)
                f2.close()
            print('Configuration sauvegardée !')
            
        addPushButton.clicked.connect(add_path)
        rmPushButton.clicked.connect(rm_path)
        runPushButton.clicked.connect(run)
        savePushButton.clicked.connect(save_param)

if __name__ == '__main__':

    import sys
    
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_()) 
