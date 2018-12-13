# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class Cas(QTableWidget):

    def __init__(self, *__args):
        QTableWidget.__init__(self, *__args)

    def mouseReleaseEvent(self, *args, **kwargs):
        print(self.currentRow())
        self.selectRow(self.currentRow())
        super(Cas, self).mouseReleaseEvent(*args, **kwargs)

    def dragMoveEvent(self, e):
        print('=df')
        e.accept()

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
        self.listWidget_3 = QtWidgets.QListWidget(Form)
        self.listWidget_3.setGeometry(QtCore.QRect(480, 40, 431, 241))
        self.listWidget_3.setObjectName("listWidget_3")
        self.listWidget_2 = QtWidgets.QListWidget(Form)
        self.listWidget_2.setGeometry(QtCore.QRect(20, 40, 431, 241))
        self.listWidget_2.setObjectName("listWidget_2")
        self.tableWidget = Cas(Form)
        self.tableWidget.setGeometry(QtCore.QRect(100, 280, 656, 192))
        self.tableWidget.setObjectName("tableWidget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

