# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidgetItem, QHeaderView, QMainWindow, \
    QGridLayout, QTableWidget, QTableWidgetItem, QFrame, QAbstractItemView
import time
import ftplib
from pathlib import Path
import re
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMenu


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
                pixmap = QtGui.QPixmap(label.size())
                label.render(pixmap)
                drag.setPixmap(QtGui.QPixmap(obj.icon().pixmap(label.size())))
                #drag.setPixmap(pixmap)
                a = drag.exec_()
                #dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)
                #mimeData.setData("application/x-hotspot",)
            # self.selectRow(self.rowAt(e.pos().y()))

        except Exception as err:
            print(err)

    def dragMoveEvent(self, e):
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
        self.ftp_upload_obj = None
        self.host_path_link = None

    def contextMenuEvent(self, pos):
        try:
            menu = QMenu()
            pass_co = menu.addAction('pass')
            deletion = menu.addAction('Delete')
            action = menu.exec_(QCursor.pos())
            if action == deletion:
                self.remove_host_file(self.currentItem().text())
        except Exception as err:
            print(err)

    def remove_host_file(self, file):
        item_permission = self.item(self.currentRow(), 2).text()
        if item_permission[0] != 'd':
            try:
                self.ftp_upload_obj.delete(file)
            except Exception as err:
                print(err)
        else:
            try:
                self.ftp_upload_obj.rmd(file)
            except Exception as err:
                items = self.ftp_upload_obj.nlst(file)
                self.ftp_upload_obj.cwd(file)
                print(items)
                if items[0] != '.' and items[1] != '..':
                    [self.ftp_upload_obj.delete(file_dir) for file_dir in items]
                else:
                    [self.ftp_upload_obj.delete(file_dir) for file_dir in items[2:]]
                print(self.host_path_link)
                #self.host_path_link.pop()
                self.ftp_upload_obj.cwd(self.host_path_link[-1])
                self.ftp_upload_obj.rmd(file)
                self.server_files(self.host_path_link[-1], self.ftp_upload_obj)


    def dragMoveEvent(self, e):
        #e.setDropAction(QtCore.Qt.CopyAction)
        print('drag move')
        #e.accept()

    def dropEvent(self, e):
        list_of_items = []
        [list_of_items.append(self.item(table_item, 0).text()) for table_item in range(self.rowCount())]
        print(list_of_items[1:])
        print(e.mimeData())
        icon = f'{start_path}\icons\{"dir_icon.png" if e.mimeData().hasFormat("application/directory") else "file_icon.png"}'
        if e.mimeData().text() not in list_of_items[1:]:
            try:
                self.setRowCount(self.rowCount() + 1)
                item = QTableWidgetItem(e.mimeData().text())
                item.setIcon(QIcon(icon))
                self.setItem(self.rowCount()-1, 0,item)
                if e.mimeData().hasFormat("application/directory"):
                    self.ftp_upload_obj.mkd(e.mimeData().text())
                    self.ftp_upload_obj.cwd(e.mimeData().text())
                    #print(e.mimeData().text())
                    print(os.path.abspath(e.mimeData().text()))
                self.upload_files(os.path.abspath(e.mimeData().text()), self.ftp_upload_obj)
                e.accept()
                self.server_files(self.host_path_link[-1], self.ftp_upload_obj)
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
    def server_files(self, cwd, ftp_obj):
        try:
            files_list = []
            ftp_obj.cwd(cwd)
            # callback функция для занесения файлв в список вместо стандартного stdout callback
            custom_callback = lambda n: files_list.append(n)
            # получить список файлов с сервера
            ftp_obj.retrlines('LIST', custom_callback)

            self.setRowCount(len(files_list) + 1)
            self.setItem(0, 0, QTableWidgetItem('...'))
            for num, file in enumerate(files_list, start=1):
                permissions = re.search(r'^[-]?[\w+-]*', file).group()
                name = re.search(r'[\w_-]*[].?[\w+]*$', file).group()
                date = re.search(r'\w+\s{0,2}\d+ \s{0,3}\d+[:]?\d+',file).group()
                file_rights = re.findall(r'(^[-\w]*)', file)[0]

                file_name = QTableWidgetItem(name)
                modified_time = QTableWidgetItem(date)
                icon = f'{start_path}\icons\dir_icon.png' if permissions[0] == 'd' else r'%s\icons\file_icon.png' % start_path
                file_name.setIcon(QIcon(icon))

                self.setItem(num, 0, QTableWidgetItem(file_name))
                self.setItem(num, 1, QTableWidgetItem(modified_time))
                self.setItem(num, 2, QTableWidgetItem(file_rights))
        except ftplib.error_perm:
            self.server_files('/', ftp_obj)
        except Exception as err:
            print(err)

    def test(self, path, ftp_obj):
        walk = list(os.walk(path))[0]
        for file in walk[2]:
            fh = open(walk[0] + r'\\' + file, 'rb')
            ftp_obj.storbinary('STOR %s' % file, fh)
            fh.close()
        while len(walk[1]) != 0:
            print(walk[1][0])
            ftp_obj.mkd(walk[1][0])
            ftp_obj.cwd(walk[1][0])
            self.test(path + r'\%s' % walk[1][0], ftp_obj)
            try:
                ftp_obj.cwd('/' + os.path.basename(Path(walk[0]).parents[0]))
            except:
                pass
            walk[1].pop(0)
            # fh = open(f, 'rb')
            # ftp_obj.storbinary('STOR %s' % f, fh)
            # fh.close()

    def upload_files(self, path, ftp_obj):
        self.test(path, ftp_obj)
        # files = os.listdir(path)
        # os.chdir(path)
        # files_list = []
        # dirs_list = []
        # [files_list.append(file) for file in files if os.path.isfile(path + r'\{}'.format(file))]
        # print('files', files)
        # for f in files:
        #     print(os.getcwd())
        #     print(os.path.isfile(path + r'\{}'.format(f)))
        #     if os.path.isfile(path + r'\{}'.format(f)):
        #         fh = open(f, 'rb')
        #         ftp_obj.storbinary('STOR %s' % f, fh)
        #         fh.close()
        #     elif os.path.isdir(path + r'\{}'.format(f)):
        #         ftp_obj.mkd(f)
        #         ftp_obj.cwd(f)
        #         self.upload_files(path + r'\{}'.format(f), ftp_obj)
        # ftp_obj.cwd('/')
        # os.chdir('..')


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(990, 630)
        self.line_ip = QLineEdit(self)
        self.line_ip.setPlaceholderText('address')
        self.line_ip.move(20, 20)
        self.line_ip.resize(200, 25)

        self.line_username = QLineEdit(self)
        self.line_username.setPlaceholderText('username')
        self.line_username.move(250, 20)
        self.line_username.resize(200, 25)

        self.line_password = QLineEdit(self)
        self.line_password.setPlaceholderText('password')
        self.line_password.move(480, 20)
        self.line_password.resize(200, 25)

        self.pybutton = QPushButton('Connect', self)
        self.pybutton.resize(200, 32)
        self.pybutton.move(700, 20)

        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(120, 320, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 340, 891, 231))
        self.listWidget.setObjectName("listWidget")
        self.hostWidget = HostTable(Form)
        self.hostWidget.setGeometry(QtCore.QRect(480, 60, 431, 241))
        self.hostWidget.setObjectName("hostWidget")
        self.tableWidget = LocalTable(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 431, 241))
        self.tableWidget.setObjectName("tableWidget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

