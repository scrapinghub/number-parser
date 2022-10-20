#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='number-parser',
    version='0.3.0',
    description='parse numbers written in natural language',
    long_description=open('README.rst', encoding="utf8").read() + "\n\n" + open('CHANGES.rst').read(),
    author='Arnav Kapoor',
    author_email='arnavk805@gmail.com',
    url='https://github.com/arnavkapoor/number-parser',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'attrs >= 17.3.0',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
