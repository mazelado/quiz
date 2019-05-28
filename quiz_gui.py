#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/22/19 3:40 PM

@author: matt
"""
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from quiz_uic import Ui_MainWindow


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
