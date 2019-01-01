# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os
import time
import ftplib
from pathlib import Path
import re
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMenu, QAbstractItemView


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

    def mousePressEvent(self, e):
        label = self.childAt(e.pos())

        try:
            super(LocalTable, self).mousePressEvent(e)
            a = self.selectedItems()
            for obj in a:
                mimeData = QtCore.QMimeData()
                data = QtCore.QByteArray()
                app_type = "application/directory" if os.path.isdir(obj.text()) else "application/file"
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

    def dir_download(self, path, cwd, ftp_obj):
        files = path.nlst()
        for file in files:
            try:
                file_obj = open(os.getcwd() + file, 'wb')
                ftp_obj.retrbinary('RETR %s' % file, ftp_obj)
                file_obj.close()
            except Exception as err:
                print(err)
                os.mkdir(os.getcwd() + file)
                ftp_obj.cwd(file)
                self.dir_download(path, cwd, ftp_obj)
                ftp_obj.cwd(path)



        # try:
        #     files = ftp_obj.nlst(path)
        #     dirs_list = []
        #     for file in files:
        #         try:
        #             ftp_obj.delete(file)
        #             print(file)
        #         except Exception as err:
        #             dirs_list.append(file) if file != '.' and file != '..' and file != '...' else None
        #     while len(dirs_list) != 0:
        #         try:
        #             ftp_obj.rmd(dirs_list[0])
        #         except:
        #             ftp_obj.cwd(dirs_list[0])
        #             self.dirs_deletion(ftp_obj.pwd(), cwd, ftp_obj)
        #             ftp_obj.cwd(path)
        #         ftp_obj.rmd(dirs_list[0])
        #         dirs_list.pop(0)
        # except Exception as err:
        #     pass

    def contextMenuEvent(self, pos):
        try:
            menu = QMenu()
            pass_co = menu.addAction('pass')
            deletion = menu.addAction('Delete')
            action = menu.exec_(QCursor.pos())
            if action == deletion:
                to_delete_dict = dict()
                for n, item in enumerate(self.selectedItems()):
                    if n % 3 == 0 and self.item(item.row(), 2).text()[0] == 'd':
                        to_delete_dict.update({self.item(item.row(), 0).text(): self.item(item.row(), 2).text()[0]})
                    elif n % 3 == 0 and self.item(item.row(), 2).text()[0] == '-' or self.item(item.row(), 2).text()[0] == 'r':
                        to_delete_dict.update({self.item(item.row(), 0).text():self.item(item.row(), 2).text()[0]})

                current_host_cwd = self.ftp_upload_obj.pwd()
                for file in to_delete_dict:
                    if to_delete_dict[file] == 'd':
                        #current_host_cwd = self.ftp_upload_obj.pwd()
                        self.ftp_upload_obj.cwd(file)
                        self.dirs_deletion(self.ftp_upload_obj.pwd(), file, self.ftp_upload_obj)
                        self.ftp_upload_obj.cwd(current_host_cwd)
                        self.ftp_upload_obj.rmd(file)

                    else:
                        self.ftp_upload_obj.delete(file)
                self.server_files(current_host_cwd, self.ftp_upload_obj)
        except Exception as err:
            print(err)

    def dirs_deletion(self, path, cwd, ftp_obj):
        try:
            files = ftp_obj.nlst(path)
            dirs_list = []
            for file in files:
                try:
                    ftp_obj.delete(file)
                    print(file)
                except Exception as err:
                    dirs_list.append(file) if file != '.' and file != '..' and file != '...' else None
            while len(dirs_list) != 0:
                try:
                    ftp_obj.rmd(dirs_list[0])
                except:
                    ftp_obj.cwd(dirs_list[0])
                    self.dirs_deletion(ftp_obj.pwd(), cwd, ftp_obj)
                    ftp_obj.cwd(path)
                ftp_obj.rmd(dirs_list[0])
                dirs_list.pop(0)
        except Exception as err:
            pass

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        #list_of_items = []
        #[list_of_items.append(self.item(table_item, 0).text()) for table_item in range(self.rowCount())]
        #print(list_of_items[1:])
        #print(e.mimeData())
        icon = f'{start_path}\icons\{"dir_icon.png" if e.mimeData().hasFormat("application/directory") else "file_icon.png"}'
        # if e.mimeData().text() not in list_of_items[1:]:
        try:
            self.setRowCount(self.rowCount() + 1)
            item = QTableWidgetItem(e.mimeData().text())
            item.setIcon(QIcon(icon))
            self.setItem(self.rowCount()-1, 0,item)
            d = os.getcwd()
            if e.mimeData().hasFormat("application/directory"):
                self.ftp_upload_obj.mkd(e.mimeData().text())
                self.ftp_upload_obj.cwd(e.mimeData().text())
                self.upload_files(os.path.abspath(e.mimeData().text()), self.ftp_upload_obj)
            else:
                fh = open(d + r'\\' + e.mimeData().text(), 'rb')
                self.ftp_upload_obj.storbinary('STOR %s' % e.mimeData().text(), fh)
                fh.close()
            #e.accept()

            self.server_files(self.host_path_link[-1], self.ftp_upload_obj)
        except Exception as err:
            print(err)
    # else:
    #     print('exist')
    #     e.ignore()
        #print(self.rowAt(e.pos()))
        #print(self.rowAt(e.pos().y()))

    def dragEnterEvent(self, e):
        e.accept()

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

    def upload_files(self, path, ftp_obj):
        walk = list(os.walk(path))[0]
        for file in walk[2]:
            fh = open(walk[0] + r'\\' + file, 'rb')
            ftp_obj.storbinary('STOR %s' % file, fh)
            fh.close()
        while len(walk[1]) != 0:
            print(walk[1][0])
            ftp_obj.mkd(walk[1][0])
            ftp_obj.cwd(walk[1][0])
            self.upload_files(path + r'\%s' % walk[1][0], ftp_obj)
            try:
                ftp_obj.cwd('/' + os.path.basename(Path(walk[0]).parents[0]))
            except:
                pass
            walk[1].pop(0)

   # def upload_files(self, path, ftp_obj):
        #self.test(path, ftp_obj)
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

