#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import io
import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', os.linesep)
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_install_requires():
    content = read(os.path.join(
            os.path.dirname(__file__), 'requirements', 'base.txt'))
    return content.strip().split(os.linesep)

def read_version():
    content = read(os.path.join(
            os.path.dirname(__file__), 'integrador_fiscal', '__init__.py'))
    return re.search(r"__version__ = '([^']+)'", content).group(1)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'satcfe=='
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(kmee): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='integrador_fiscal',
    version=read_version(),
    description="Python Integrador Fiscal Sefaz Ceara (MF-e, ct-e, vfp-e)",
    long_description=readme + '\n\n' + history,
    author="KMEE INFORMATICA LTDA",
    author_email='contato@kmee.com.br',
    url='https://github.com/kmee/integrador_fiscal',
    packages=find_packages(include=['integrador_fiscal']),
    entry_points={
        'console_scripts': [
            'integrador_fiscal=integrador_fiscal.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=read_install_requires(),
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='integrador_fiscal',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
