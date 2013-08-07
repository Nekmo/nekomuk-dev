#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
¿Tienes una gran cantidad de archivos multimedia y necesitas poder
ver lo que tienes desde cualquier lugar y en cualquier momento?
Nekomuk te permite crear una biblioteca web de aquellos discos duros
que desees, almacenando de los archivos sus propiedades, tamaño, md5,
una previsualización, y mucho más. Es perfecto para poder ver desde
cualquier lugar si tenías esa película que no recordabas tener,
aunque ese disco duro se encuentre desconectado.
"""

import os
# from setuptools import setup, find_packages

def include_data(path):
    include = []
    for root, dirs, files in os.walk(path):
        list_files = []
        include.append([root, list_files])
        for file in files:
            list_files.append('%s/%s' % (root, file))
    return include

# setup(
#     name = "nekomuk",
#     version = "0.2",
#     packages = find_packages(),
#     scripts = ['nekomuk-admin.py'],

#     install_requires = ['lxml', 'kaa_metadata'],
#     package_data = {
#         'nekomuk/share': include_data('nekomuk/share'),
#     },

#     # metadata for upload to PyPI
#     author = "Nekmo",
#     author_email = "contacto@nekmo.com",
#     description = "Biblioteca multimedia offline",
#     license = "GPL",
#     keywords = "multimedia library",
#     url = "http://nekmo.com",   # project home page, if any

#     # could also include long_description, download_url, classifiers, etc.
# )

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = [
    'nekomuk/*', 'nekomuk/share/*', 'nekomuk/infodevice/*'
]

setup(name = "nekomuk",
    version = "20",
    description = "Biblioteca multimedia offline",
    author = "Nekmo",
    author_email = "contacto@nekmo.com",
    url = "http://nekmo.com",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['nekomuk', 'nekomuk.infodevice'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'nekomuk' : files },
    data_files=include_data('nekomuk/share'),
    #'runner' is in the root.
    scripts = ["nekomuk-admin.py"],
    long_description = __doc__,
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     
) 