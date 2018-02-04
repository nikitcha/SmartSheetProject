# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Smart Music Sheet',
    version='0.1.0',
    description='Music Sheet Score Following',
    long_description=readme,
    author='Nikolay Tchakarov, Alexis Nortier',
    author_email='nikitcha@gmail.com',
    url='https://github.com/nikitcha/SmartSheetProject',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

