#!/usr/bin/env python

import codecs
import os
import sys

from setuptools import setup

version = '1.0.1'

# Stolen from Kenneth Reitz
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('python setup.py bdist_wheel --universal')
    os.system('twine upload dist/lazyreader-%s*' % version)
    sys.exit()


def read(f):
    return codecs.open(f, encoding='utf-8').read()


setup(
    name='lazyreader',
    version=version,
    description='Lazy reading of file objects for efficient batch processing',
    long_description=read('README.rst'),
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    url='https://github.com/alexwlchan/lazyreader',
    py_modules=['lazyreader'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    )
)
