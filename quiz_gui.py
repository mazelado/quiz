#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/22/19 3:40 PM

@author: matt
"""
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([])

label = QLabel('Hello, World!')
label.show()

app.exec_()