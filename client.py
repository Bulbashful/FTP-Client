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
        self.hostWidget.server_files()
        #self.tableWidget.cellClicked.connect(self.cellClick)
        self.tableWidget.doubleClicked.connect(self.catch_double_click)
        #self.listWidget_2.dragEnabled()

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

    # def cellClick(self, p_int, p_int_1):
    #     print('+')
    #     pass
        # if p_int == 0:
        #     above_path = os.chdir(os.path.dirname(os.getcwd()))
        #     self.tableWidget.local_files(os.listdir(above_path))
        # else:
        #     print(self.tableWidget.item(p_int, p_int_1))
        #     pass
        #     #icon = f'{current_path}\icons\{"dir_icon.png" if os.path.isdir(file) else "file_icon.png"}'







def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()