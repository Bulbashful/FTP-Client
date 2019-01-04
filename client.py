# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import design
import sys
import os
import ftplib


class ExampleApp(QtWidgets.QMainWindow, design.Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.local_files(os.listdir(os.getcwd()))
        self.host_cwd = ['/']
        self.hostWidget.host_path_link = self.host_cwd
        self.tableWidget.doubleClicked.connect(self.catch_double_click)
        self.hostWidget.doubleClicked.connect(self.catch_host_double_click)
        self.pybutton.clicked.connect(self.ftp_connector)
        self.tableWidget.table_bar_obj = self.listWidget
        self.ftp_obj = None
        self.listWidget.setColumnCount(2)
        self.hostWidget.table_bar_obj = self.listWidget
        self.listWidget.setColumnWidth(0,200)
        self.listWidget.setColumnWidth(1, 689)
        self.listWidget.setHorizontalHeaderLabels(['Progress', 'Path'])
        self.listWidget.verticalHeader().hide()
        self.listWidget.setShowGrid(False)

    def ftp_connector(self):
        self.hostWidget.clear()
        if not self.line_ip.text() == '':
            try:
                ftp = ftplib.FTP(self.line_ip.text(), self.line_username.text(), self.line_password.text())
                try:
                    ftp.login()
                except:
                    pass
                self.ftp_obj = ftp
                self.hostWidget.ftp_upload_obj = ftp
                self.tableWidget.ftp_obj = ftp
                self.hostWidget.clear()
                return self.hostWidget.server_files('/', self.ftp_obj)
            except:
                self.message_box('Not valid data')
        else:
            self.message_box('Server address field is empty')

    def message_box(self, str_info):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle('Error')
        msg.setText(str_info)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def catch_double_click(self):
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).text()
        try:
            if self.tableWidget.currentRow() == 0:
                os.chdir(os.path.dirname(os.getcwd()))
                self.tableWidget.local_files(os.listdir(os.getcwd()))
                pass
            elif os.path.isdir(selected_item):
                os.chdir(os.getcwd() + f'\{selected_item}')
                self.tableWidget.local_files(os.listdir(os.getcwd()))
        except:
            pass

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
            except:
                pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.setWindowTitle('FTP-Client')
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()