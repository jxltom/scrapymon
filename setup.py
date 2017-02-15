#!/usr/bin/env python

from setuptools import setup, find_packages

from flask_boilerplate import __version__, __author__

setup(
    name='flask-boilerplate',
    version=__version__,
    description='A boilerplate for Flask applications',
    long_description=open('README.md').read(),
    keywords='bootstrap authentication http-basic-auth sqlalchemy celery '
             'smtp-mail heroku wechat-official-account scheduling',
    author=__author__,
    author_email='jxltom@gmail.com',
    url='https://github.com/jxltom/flask-boilerplate/',
    license='MIT',

    packages=find_packages(),
    install_requires=['requests>=2.11.0'],

    entry_points={
        'console_scripts': [
            'flask_boilerplate = flask_boilerplate.__main__:main'
        ],
    },
)
