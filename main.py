#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MultiCompile v0.3-alpha
Généré le 11 Juillet 2019
@author: Th. G

Ce logiciel est mis à disposition sous licence Creatice Commons 
(Pas d'utilisation commerciale, Partage dans les mêmes conditions).
"""

import re
from subprocess import call
import os
import sys
import platform
system = platform.system()
if system == "Linux" :
    pass
else :
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from pathlib import Path
from shutil import copyfile
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog, QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, 
                             QHBoxLayout, QLabel, QPushButton, QScrollBar, QSizePolicy, QTextEdit,
                             QTableWidget, QTabWidget, QVBoxLayout, QWidget, QTableWidgetItem,
                             QHeaderView)



class main(QDialog):
    
   
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        
        GroupBox = QGroupBox("Emplacements")
        GroupBox.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)
        
        def createtable(self):
            tableWidget.setHorizontalHeaderLabels(["Emplacement", "Nom", "Ouvrir", "Supprimer" ]) 
            rows = tableWidget.rowCount()
            columns = tableWidget.columnCount()
            for i in range(rows):
                for j in range(columns):
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled)
                    tableWidget.setItem(i, j, item)

        tableWidget = QTableWidget(1, 4)
        createtable(self)
        header = tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        GroupBoxLayout = QVBoxLayout()
        GroupBoxLayout.setContentsMargins(5, 5, 5, 5)
        GroupBoxLayout.addWidget(tableWidget)
        addPushButton = QPushButton("Ajouter un emplacement")
        addPushButton.setDefault(True)
        GroupBoxLayout.addWidget(addPushButton)
        GroupBoxLayout.addStretch(1)
        GroupBox.setLayout(GroupBoxLayout)
        
        
        LogBox = QTabWidget()
        
        
        # Initialize tab screen
        tab1 = QWidget()
        tab2 = QWidget()
        

        LogBox.addTab(tab1,"Log")
        LogBox.addTab(tab2,"Détails")
        

        tab1.layout = QVBoxLayout(self)
        
        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        log = "Bienvenue dans MultiCompile !\n"
        textEdit.setPlainText(log)
 
        tab1.layout.addWidget(textEdit)
        tab1.setLayout(tab1.layout)
        
        tab2.layout = QVBoxLayout(self)
        
        textEdit2 = QTextEdit()
        textEdit2.setReadOnly(True)
        latex = "Opérations terminées !\n" + "Les fichiers suivants vous donneront plus d'informations sur les opérations de compilation et les erreurs :\n"
        LogBox.setTabEnabled(1,False)
        textEdit2.setPlainText(latex)
 
        tab2.layout.addWidget(textEdit2)
        tab2.setLayout(tab2.layout)
        
        
                
        ParamBox = QGroupBox("Paramètres")
        compilerComboBox = QComboBox()
        compilerComboBox.addItems(["pdflatex","xelatex"])
        savePushButton = QPushButton("Sauvegarder")
        savePushButton.setDefault(True)
        #logPushButton = QPushButton("Voir le log")
        runPushButton = QPushButton("Compiler !")
        runPushButton.setStyleSheet("background-color: green; color: white")
        
        try :
            f= open(Path(os.path.dirname(os.path.realpath(__file__)) + '/' +  "config.txt"),"r")
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
            f= open(Path(os.path.dirname(os.path.realpath(__file__)) + '/' + "config.txt"),"w+")
            contents = ["pdflatex"]
            with open(Path(os.path.dirname(os.path.realpath(__file__))  + '/' +  "config.txt"), "w") as f:
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
            def refresh_textedit2(MYSTRING): 
                textEdit2.append(str(MYSTRING)) #append string
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
                    f = open(Path(mypath + "/master.tex"),"r")
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
                        nonstopmode = '-halt-on-error'
                        jobname = '-jobname=' + chapter + '_' + h + '-' + 'master'
                        options = '"\input{master}"'
                        compiler = str(compilerComboBox.currentText())
                        refresh_textedit("Compilation en cours...")
                        success = call([compiler, nonstopmode, jobname, options])
                        if success == 0 :
                            try:
                                os.mkdir(Path(init_path + '/output'))
                            except FileExistsError:
                                pass
                            try:
                                copyfile(Path(mypath + '/' + chapter + '_' + h + '-' + 'master' + '.pdf') ,Path(init_path + 'output/' + chapter + '_' + h + '-' + 'master' + '.pdf'))
                            except FileNotFoundError:
                                refresh_textedit('Une erreur est survenue lors de la copie du pdf...')
                                error+=1
                        else :
                            error+=1
                            pass
                        
                        refresh_textedit2(Path(mypath + '/' + chapter + '_' + h + '-' + 'master' + '.log'))
                        refresh_textedit('Compilation de "' + h + '" terminée avec ' + str(error) + ' erreur(s).')
                    else :
                        refresh_textedit('Les audiences trouvées dans "' + h + '" sont : ' + str(audiences) + '.')
                        refresh_textedit(str(len(audiences)) + ' documents pdf seront créés !\n' + 'Compilation en cours...')
                        
                        for j in audiences :
                            call('cd ' + mypath, shell=True)
                            nonstopmode = '-halt-on-error'
                            jobname = '-jobname=' + chapter + '_' + h + '-' + j
                            options = '"\def\CurrentAudience{' + j + '}\input{master}"'
                            compiler = str(compilerComboBox.currentText())
                            success = call([compiler, nonstopmode, jobname, options])
                            if success == 0 :
                                try:
                                    os.mkdir(Path(init_path + '/output'))
                                except FileExistsError:
                                    pass
                                try:
                                    copyfile(Path(mypath + '/' + chapter + '_' + h + '-' + j + '.pdf') , Path(init_path + 'output/' + chapter + '_' + h + '-' + j + '.pdf'))
                                except FileNotFoundError:
                                    refresh_textedit('Une erreur est survenue lors de la copie du pdf...')
                                    error+=1
                            else :
                                error+=1
                                pass
                            
                            refresh_textedit2(Path(mypath + '/' + chapter + '_' + h + '-' + j + '.log'))
                            #os.system('xdg-open ' + name + '-' + j + '.pdf > /dev/null')
                        
                        #LogBox.setCurrentWidget(tab1)
                        refresh_textedit('Compilation de "' + h + '" terminée avec ' + str(error) + ' erreur(s).')

                
                if os.path.exists(Path(init_path + '/master.tex')):
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
                        
            LogBox.setTabEnabled(1,True)
            LogBox.setCurrentWidget(tab2)
                    
        def add_path() :
            file = str(QFileDialog.getExistingDirectory(self, "Selectionner un dossier"))
            rowPosition = tableWidget.rowCount()
            item = QTableWidgetItem()
            item.setText(file+'/')
            tableWidget.setItem(rowPosition-1, 0, item)
            chapter = QTableWidgetItem()
            chapter.setText(os.path.basename(os.path.normpath(file)))
            tableWidget.setItem(rowPosition-1, 1, chapter)
            viewPushButton = QPushButton(tableWidget)
            viewPushButton.setText('Ouvrir')
            tableWidget.setCellWidget(rowPosition-1, 2, viewPushButton)
            rmPushButton = QPushButton(tableWidget)
            rmPushButton.setText('Supprimer')
            tableWidget.setCellWidget(rowPosition-1, 3, rmPushButton)
            tableWidget.insertRow(rowPosition)
            rmPushButton.clicked.connect(rm_path)
            viewPushButton.clicked.connect(open_path)
        
        def open_path() :
            button = QApplication.focusWidget()
            index = tableWidget.indexAt(button.pos())
            location = str(tableWidget.item(index.row(), 0).text())
            system = platform.system()
            if system == "Linux" :
                os.system('xdg-open "%s"' % location)
            else :
                os.startfile(location)

        def rm_path(self) :
            button = QApplication.focusWidget()
            index = tableWidget.indexAt(button.pos())
            tableWidget.removeRow(index.row())
            
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
        runPushButton.clicked.connect(run)
        savePushButton.clicked.connect(save_param)

if __name__ == '__main__':

    import sys
    
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_()) 
