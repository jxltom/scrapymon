#!/usr/bin/env python

from setuptools import setup, find_packages

from flask_boilerplate import __version__, __author__

setup(
    name='scrapymon',
    version=__version__,
    description='Simple management UI for scrapyd',
    long_description=open('README.md').read(),
    author=__author__,
    author_email='jxltom@gmail.com',
    url='https://github.com/jxltom/scrapymon/',
    license='MIT',

    include_package_data=True,

    packages=find_packages(),
    install_requires=[
        'flask==0.12',
        'Flask-Bootstrap==3.3.7.0',
        'Flask-SQLAlchemy==2.1',
        'mysql-connector==2.1.4',
        'Flask-BasicAuth==0.2.0',
        'Flask-Mail==0.9.1',
        'arrow==0.10.0',
        'celery==4.0.2',
        'redis==2.10.5',
        'gevent==1.2.1',
        'requests==2.13.0',
        'scrapyd==1.2.0a1',
    ],
    dependency_links=[
        'git+https://github.com/jxltom/easy-scheduler.git@0.1.0#egg=easy-scheduler',
        'git+https://github.com/jxltom/flask-security.git@edf3e89#egg=Flask-Security',
        'git+https://github.com/flask-admin/flask-admin.git@0795a3f#egg=Flask-Admin',
        'git+https://github.com/whtsky/WeRoBot.git@7269d6b#egg=WeRoBot',
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
