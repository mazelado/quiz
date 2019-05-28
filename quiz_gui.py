#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/22/19 3:40 PM

@author: matt
"""
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from quiz_uic import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        print('entering MainWindow.__init__')
        super(MainWindow, self).__init__()

        # Set up the user interface from Qt Designer
        self.setupUi(self)

        # Make some local modifications

        # Connect the controls
        # Buttons
        self.pushButton_add.clicked.connect(self.pushButton_add_clicked)
        self.pushButton_edit.clicked.connect(self.pushButton_edit_clicked)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)
        # Menu
        self.action_quit.triggered.connect(self.action_quit_triggered)

        # Populate the data
        print('exiting MainWindow.__init__')

    def pushButton_add_clicked(self):
        print('entering MainWindow.pushButton_add_clicked')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Add question?')
        msg.setWindowTitle('Add')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()
        print('Value of pressed message box button:', retval)
        print('exiting MainWindow.pushButton_add_clicked')

    def pushButton_edit_clicked(self):
        print('inside pushButton_edit_clicked')

    def pushButton_delete_clicked(self):
        print('inside pushButton_delete_clicked')

    def action_quit_triggered(self):
        print('inside quit method')
        sys.exit()


def main():
    print('entering main')
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    print('exiting main')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
