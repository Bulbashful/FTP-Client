# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidgetItem, QHeaderView, QMainWindow, \
    QGridLayout, QTableWidget, QTableWidgetItem, QFrame, QAbstractItemView
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from ftplib import FTP
import design
import sys
import os
import ftplib
from pathlib import Path
import pathlib
import time
import re


class ExampleApp(QtWidgets.QMainWindow, design.Ui_Form):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # занесение файлов в list widget и прикпреплние иконки в зависимости от типа файла
        # передать файлы текущеё рабочей директории
        self.tableWidget.local_files(os.listdir(os.getcwd()))
        self.host_cwd = ['/']
        self.hostWidget.host_path_link = self.host_cwd
        # print(self.host_cwd[-3])
        # self.hostWidget.server_files(self.host_cwd[-3])
        #self.tableWidget.cellClicked.connect(self.cellClick)
        self.tableWidget.doubleClicked.connect(self.catch_double_click)
        self.hostWidget.doubleClicked.connect(self.catch_host_double_click)
        self.pybutton.clicked.connect(self.ftp_connector)
        #self.listWidget_2.dragEnabled()
        self.ftp_obj = None

    def ftp_connector(self):
        #ftp = ftplib.FTP('92.242.39.60','')
        try:
            print(self.line_ip.text(), self.line_username.text(), self.line_password.text())
            ftp = ftplib.FTP(self.line_ip.text(), self.line_username.text(), self.line_password.text())
            ftp = ftplib.FTP('ftp.dlptest.com', 'dlpuser@dlptest.com', 'e73jzTRTNqCN9PYAAjjn')
            try:
                ftp.login()
            except Exception as err:
                print(err)
            self.ftp_obj = ftp
            self.hostWidget.ftp_upload_obj = ftp
            return self.hostWidget.server_files('/', self.ftp_obj)
        except Exception as err:
            #TODO Alert
            print(err)

    def catch_double_click(self):
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).text()
        try:
            if self.tableWidget.currentRow() == 0:
                os.chdir(os.path.dirname(os.getcwd()))
                self.tableWidget.local_files(os.listdir(os.getcwd()))
                pass
            elif os.path.isdir(selected_item):
                # новая рабочая директория
                os.chdir(os.getcwd() + f'\{selected_item}')
                self.tableWidget.local_files(os.listdir(os.getcwd()))
        except:
            #TODO add alert
            print('Error')

    def catch_host_double_click(self):
        selected_item = self.hostWidget.item(self.hostWidget.currentRow(), self.hostWidget.currentColumn()).text()
        item_permission = None
        try:
            item_permission = self.hostWidget.item(self.hostWidget.currentRow(), 2).text()
        except:
            pass
        if item_permission is None:
            self.host_cwd.pop()
            self.hostWidget.server_files(self.host_cwd[-1], self.ftp_obj)
        elif item_permission[0] == 'd':
            try:
                self.host_cwd.append(f'/{selected_item}')
                self.hostWidget.server_files(selected_item, self.ftp_obj)
            except Exception as err:
                print(err)
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()