#!/usr/bin/env python

from distutils.core import setup

setup(  name='cssp',
        version='0.1.0',
        description='CSS Preprocessor',
        author='Francisco Pinzon (Pacho)',
        author_email='pacho@bitremix.com',
        url='http://github.com/fpinzn/cssp',
        license='GPL v3.0',
        py_modules=['ply'],
        scripts=['css_lexer.py','css_parser.py']
     )
