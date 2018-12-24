# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidgetItem, QHeaderView, QMainWindow, \
    QGridLayout, QTableWidget, QTableWidgetItem, QFrame, QAbstractItemView
import time
import ftplib
import re
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class LocalTable(QTableWidget):

    def __init__(self, *__args):
        QTableWidget.__init__(self, *__args)
        global start_path
        start_path = os.getcwd()
        self.setColumnCount(2)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(['File', 'Last modified date'])
        self.setDragEnabled(True)
        self.verticalHeader().hide()

        #self.setSelectionBehavior(QTableWidget.SelectRows)
        #self.columnAt(2)

    def mousePressEvent(self, e):
        label = self.childAt(e.pos())

        try:
            super(LocalTable, self).mousePressEvent(e)
            a = self.selectedItems()
            for obj in a:
                mimeData = QtCore.QMimeData()
                data = QtCore.QByteArray()
                app_type = "application/directory" if os.path.isdir(self.currentItem().text()) else "application/file"
                mimeData.setData(app_type, data)
                mimeData.setText(obj.text())

                drag = QtGui.QDrag(self)
                drag.setMimeData(mimeData)
                print(mimeData.text())
                pixmap = QtGui.QPixmap(label.size())
                label.render(pixmap)
                drag.setPixmap(QtGui.QPixmap(obj.icon().pixmap(label.size())))
                #drag.setPixmap(pixmap)
                a = drag.exec_()
            print(a)
                #dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)
                #mimeData.setData("application/x-hotspot",)
            # self.selectRow(self.rowAt(e.pos().y()))

        except Exception as err:
            print(err)

    def dragMoveEvent(self, e):
        print('+')
        print(self.currentItem())
        e.accept()

    def local_files(self, path_items):
        self.setRowCount(len(path_items)+1)
        self.setItem(0, 0, QTableWidgetItem('...'))

        for num, file in enumerate(path_items, start=1):
            modified_time = os.path.getmtime(file)
            custom_modified_time = time.strftime('%b %d %Y', time.localtime(modified_time))
            item = QTableWidgetItem(file)
            icon = f'{start_path}\icons\{"dir_icon.png" if os.path.isdir(file) else "file_icon.png"}'
            item.setIcon(QIcon(icon))
            #item.setTextAlignment(Qt.RightToLeft)

            #item.setFlags(QtCore.Qt.ItemIsDragEnabled)

            #.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

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
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(['File', 'Last modified date', 'Rights'])
        self.verticalHeader().hide()
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setShowGrid(False)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.ftp_obi = self.ftp_connector()


    def ftp_connector(self):
        ftp = ftplib.FTP('92.242.39.60')
        ftp.login()
        print(ftp.encoding)
        return ftp

    def dragMoveEvent(self, e):
        #e.setDropAction(QtCore.Qt.CopyAction)
        print('drag move')
        #e.accept()

    def dropEvent(self, e):
        list_of_items = []
        [list_of_items.append(self.item(table_item, 0).text()) for table_item in range(self.rowCount())]
        print(self.rowCount())
        print(list_of_items[1:])
        icon = f'{start_path}\icons\{"dir_icon.png" if e.mimeData().hasFormat("application/directory") else "file_icon.png"}'
        if e.mimeData().text() not in list_of_items[1:]:
            try:
                self.setRowCount(self.rowCount() + 1)
                item = QTableWidgetItem(e.mimeData().text())
                item.setIcon(QIcon(icon))
                self.setItem(self.rowCount()-1, 0,item)
                e.accept()
            except Exception as err:
                print(err)
        else:
            print('exist')
            e.ignore()
        #print(self.rowAt(e.pos()))
        #print(self.rowAt(e.pos().y()))

    def dragEnterEvent(self, e):
        #e.setDropAction(QtCore.Qt.CopyAction)
        #e.acceptProposedAction()
        e.accept()


    # def dropMimeData(self, row, col, mimeData, action):
    #     print(self.last_drop_row, row)
    #     self.last_drop_row = row
    #     return True

    # def dragLeaveEvent(self, *args, **kwargs):
    #     print('host leave event')
    def server_files(self, cwd):
        try:
            files_list = []
            self.ftp_obi.cwd(cwd)
            # callback функция для занесения файлв в список вместо стандартного stdout callback
            custom_callback = lambda n: files_list.append(n)
            # получить список файлов с сервера
            self.ftp_obi.retrlines('LIST', custom_callback)

            self.setRowCount(len(files_list) + 1)
            self.setItem(0, 0, QTableWidgetItem('...'))
            for num, file in enumerate(files_list, start=1):

                    data = re.findall(r'\d+ \w+ \w+  \w+ \w+.*', file)[0].split(' ')
                    data.pop(3)
                    file_rights = re.findall(r'(^[-\w]*)', file)[0]

                    file_name = QTableWidgetItem(data[4])
                    modified_time = QTableWidgetItem(data[2] + ' ' + data[1] + ' ' + data[2])
                    icon = 'icons\dir_icon.png' if file[0] == 'd' else r'icons\file_icon.png'
                    file_name.setIcon(QIcon(icon))

                    self.setItem(num, 0, QTableWidgetItem(file_name))
                    self.setItem(num, 1, QTableWidgetItem(modified_time))
                    self.setItem(num, 2, QTableWidgetItem(file_rights))
        except ftplib.error_perm:
            self.server_files('/')
        except Exception as err:
            print(err)


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

