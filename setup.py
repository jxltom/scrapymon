#!/usr/bin/env python

from setuptools import setup, find_packages

from scrapymon import __version__, __author__

setup(
    name='scrapymon',
    version=__version__,
    description='Simple management UI for scrapyd',
    long_description=
    'Go to https://github.com/jxltom/scrapymon/ for more infomation.',
    author=__author__,
    author_email='jxltom@gmail.com',
    url='https://github.com/jxltom/scrapymon/',
    license='MIT',

    include_package_data=True,

    packages=find_packages(),
    install_requires=[
        'flask==0.12',
        'Flask-Bootstrap==3.3.7.0',
        'Flask-BasicAuth==0.2.0',
        'gevent==1.2.1',
        'requests==2.13.0',
    ],

    entry_points={
        'console_scripts': [
            'scrapymon = scrapymon.__main__:main'
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
