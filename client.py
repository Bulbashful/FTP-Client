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


class ExampleApp(QtWidgets.QMainWindow, design.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.browse_folder()
        # текущая дериктория
        # занесение файлов в list widget и прикпреплние иконки в зависимости от типа файла
        self.local_files()
        self.server_files()
        self.listWidget_2.dragEnabled()


    def local_files(self):
        current_path = os.getcwd()
        path_items = os.listdir(current_path)

        self.tableWidget.setRowCount(len(path_items))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['File', 'Last modified data'])
        self.tableWidget.setDragEnabled(True)
        self.listWidget_2.setAcceptDrops(True)

        for num, file in enumerate(path_items):
            modified_time = os.path.getmtime(file)
            custom_modified_time = time.strftime('%b %d %Y %H:%M:%S', time.localtime(modified_time))
            a = file + " " * (30-len(file)) + custom_modified_time
            print(a)
            item = QListWidgetItem(a)
            icon = 'icons\dir_icon.png' if os.path.isdir(file) else r'icons\file_icon.png'
            #item.setTextAlignment(Qt.AlignBaseline)
            item.setTextAlignment(Qt.RightToLeft)
            item.setIcon(QIcon(icon))
            item.setFlags(QtCore.Qt.ItemIsDragEnabled)
            #.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.setItem(num, 0, QTableWidgetItem(file))
            self.tableWidget.setItem(num, 1, QTableWidgetItem(custom_modified_time))
            self.listWidget_2.addItem(item)

        #self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.tableWidget.setFrameStyle(QFrame.NoFrame)
        self.tableWidget.setShowGrid(False)
        #self.tableWidget.show()


    def server_files(self):
        ftp = FTP('92.242.39.60')
        ftp.login()
        files_list = []
        # callback функция для занесения файлв в список вместо стандартного stdout callback
        custom_callback = lambda n: files_list.append(n)
        # получить список файлов с сервера
        ftp.retrlines('LIST', custom_callback)
        for file in files_list:
            item = QListWidgetItem(file)
            icon = 'icons\dir_icon.png' if file[0] == 'd' else r'icons\file_icon.png'
            item.setIcon(QIcon(icon))
            self.listWidget_3.addItem(item)

    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        #directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        # if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
        #     for file_name in os.listdir(directory):  # для каждого файла в директории
        #         self.listWidget.addItem(file_name)  # добавить файл в listWidget

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()