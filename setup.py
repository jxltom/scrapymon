#!/usr/bin/env python

from setuptools import setup, find_packages

from flask_boilerplate import __name__, __version__, __author__, \
    __author_email__

setup(
    name=__name__,
    version=__version__,
    description='sd',
    long_description=open('README.md').read(),
    keywords='login requests cookies forum discuz',
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/jxltom/requests-login/',
    license='MIT',

    packages=find_packages(),
    install_requires=['requests>=2.11.0'],

    entry_points={
        'console_scripts': [
            'flask_boilerplate = flask_boilerplate.__main__:main'
        ],
    },
)
