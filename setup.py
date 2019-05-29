#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/29/19 8:33 AM

@author: matt
"""
from distutils.core import setup

setup(
    name='Quiz',
    version='1.0dev',
    packages=['quiz_cli', 'quiz_gui', ],
    license='MIT License',
    long_description=open('README.md').read(),
)
