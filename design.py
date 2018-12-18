# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidgetItem, QHeaderView, QMainWindow, \
    QGridLayout, QTableWidget, QTableWidgetItem, QFrame, QAbstractItemView
import time
from ftplib import FTP
import re
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class LocalTable(QTableWidget):

    def __init__(self, *__args):
        QTableWidget.__init__(self, *__args)
        global current_path
        current_path = os.getcwd()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['File', 'Last modified date'])
        self.setDragEnabled(True)

    def mouseReleaseEvent(self, *args, **kwargs):
        #print(self.currentRow())
        # self.selectRow(self.currentRow())
        super(LocalTable, self).mouseReleaseEvent(*args, **kwargs)
        #super(LocalTable, self).mouseReleaseEvent(*args, **kwargs)

    def dragMoveEvent(self, e):
        print('=df')
        e.accept()

    # def cellDoubleClicked(self, p_int, p_int_1):
    #     print('dfdf')



    def mouseDoubleClickEvent(self, *args, **kwargs):
        #os.chdir(os.path.dirname(os.getcwd()))
        #print('new ', os.getcwd())
        # if self.mouseReleaseEvent(*args, **kwargs):
        #     self.local_files(os.getcwd())
        super(LocalTable, self).mouseDoubleClickEvent(*args, **kwargs)

    def local_files(self, path_items):
        path_items = os.listdir(path_items)
        print(path_items)
        self.setRowCount(len(path_items)+1)

        for num, file in enumerate(path_items, start=1):
            modified_time = os.path.getmtime(file)
            custom_modified_time = time.strftime('%b %d %Y', time.localtime(modified_time))
            item = QTableWidgetItem(file)
            icon = f'{current_path}\icons\{"dir_icon.png" if os.path.isdir(file) else "file_icon.png"}'
            item.setIcon(QIcon(icon))
            #item.setTextAlignment(Qt.AlignBaseline)
            #item.setTextAlignment(Qt.RightToLeft)

            #item.setFlags(QtCore.Qt.ItemIsDragEnabled)

            #.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.setSelectionBehavior(QTableWidget.SelectRows)
            self.setItem(num, 0, QTableWidgetItem(item))
            self.setItem(num, 1, QTableWidgetItem(custom_modified_time))

        #self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.tableWidget.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)


class HostTable(QTableWidget):

    def __init__(self, *__args):
        QTableWidget.__init__(self, *__args)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['File', 'Last modified date'])
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def mouseReleaseEvent(self, *args, **kwargs):
        print(self.currentRow())
        self.selectRow(self.currentRow())
        super(HostTable, self).mouseReleaseEvent(*args, **kwargs)

    def dragMoveEvent(self, e):
        print('=df')
        e.accept()

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print(os.getcwd())
        print(*args, **kwargs)
        super(HostTable, self).mouseDoubleClickEvent(*args, **kwargs)

    def server_files(self):
        ftp = FTP('92.242.39.60')
        ftp.login()
        files_list = []
        # callback функция для занесения файлв в список вместо стандартного stdout callback
        custom_callback = lambda n: files_list.append(n)
        # получить список файлов с сервера
        ftp.retrlines('LIST', custom_callback)

        self.setRowCount(len(files_list) + 1)

        for num, file in enumerate(files_list):
            data = re.findall(r'\d+ \w+ \w+  \w+ \w+.*', file)[0].split(' ')
            data.pop(3)

            file_name = QTableWidgetItem(data[4])
            modified_time = QTableWidgetItem(data[2] + ' ' + data[1] + ' ' + data[2])
            icon = 'icons\dir_icon.png' if file[0] == 'd' else r'icons\file_icon.png'
            file_name.setIcon(QIcon(icon))
            #print(data)
            self.setItem(num, 0, QTableWidgetItem(file_name))
            self.setItem(num, 1, QTableWidgetItem(modified_time))
        self.setShowGrid(False)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(930, 601)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(120, 320, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 340, 891, 231))
        self.listWidget.setObjectName("listWidget")
        self.hostWidget = HostTable(Form)
        self.hostWidget.setGeometry(QtCore.QRect(480, 40, 431, 241))
        self.hostWidget.setObjectName("hostWidget")
        self.tableWidget = LocalTable(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 431, 241))
        self.tableWidget.setObjectName("tableWidget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

