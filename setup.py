#!/usr/bin/env python3
# encoding: utf-8

'''
This file is a setup file to install the py1101 module and is released under the "MIT License Agreement".
'''

from setuptools import setup, find_packages

setup(
    name='py1101',
    version='1.0.0',
    url='https://github.com/10git/py1101.git',
    author='Alinux',
    description="Python3 port of the Simon Monks' clone of the ELECHOUSE_CC1101 C++ library",
    packages=find_packages(),
    install_requires=['wiringpi >= 2.60.0'],
)
