import os
from os.path import dirname, abspath, join
import re

from kombu import Queue, Exchange

import scrapymon as project


def _env(env):
    """If ENV exist but with empty value, return empty string."""
    return env if os.getenv(env) else ''


def _getenv(env, default=None):
    """If ENV doesn't exist or None, return default value."""
    # Note that os.getenv('') always returns None
    return os.getenv(_env(env), default)


class Config:
    # Settings for Flask
    SECRET_KEY = _getenv('SECRET_KEY')  # used for session
    TESTING = False

    # Settings for Flask-Webpack
    WEBPACK_MANIFEST_PATH = join(abspath(
        dirname(dirname(project.__file__))),
        'webpack-manifest.json'
    )
    print(WEBPACK_MANIFEST_PATH)

    # Settings for Flask-Basicauth
    BASIC_AUTH_USERNAME = _getenv('BASIC_AUTH_USERNAME', 'admin')
    BASIC_AUTH_PASSWORD = _getenv('BASIC_AUTH_PASSWORD', 'admin')

    # Settings for Debug by Flask-DebugToolbar
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Settings for Database by Flask-SQLAlchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Settings for Administration by Flask-Admin
    FLASK_ADMIN_SWATCH = 'simplex'

    # Settings for Celery
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_IMPORTS = ('{}.utils.celerytasks'.format(project.__name__),)

    CELERY_QUEUES = CELERY_TASK_QUEUES = (
        # Define default queue with direct exchange for project
        Queue(
            project.__name__,
            exchange=Exchange(project.__name__, type='direct'),
            routing_key=project.__name__
        ),
    )

    class CustomCeleryRouter:
        def route_for_task(self, task, args=None, kwargs=None):
            """Define task's queue, exchange (as well as its exchange type) and
            routing key. The django-celery or django-celery-beat can override
            these settings. If they are not defined here,
            queue or both exchange and routing key must set for tasks."""
            return None

    # Setup default routes for in-project's tasks
    # Compatible with both Celery 3 and 4
    CELERY_DEFAULT_QUEUE = CELERY_TASK_DEFAULT_QUEUE = project.__name__
    CELERY_DEFAULT_ROUTING_KEY = CELERY_TASK_DEFAULT_ROUTING_KEY = project.__name__
    CELERY_DEFAULT_EXCHANGE = CELERY_TASK_DEFAULT_EXCHANGE = project.__name__
    # Setup automatically routes for Celery
    CELERY_ROUTES = CELERY_TASK_ROUTES = (CustomCeleryRouter(),)

    # Applicaiton custom settings
    SCRAPYD_SERVER = _getenv('SCRAPYD_SERVER', 'http://127.0.0.1:6800')

    def __init__(self):
        if self._mail:
            mail_regex = r'(ssl|tls)://(\S+):(\S+)@(\S+):(\d+)'
            regex = re.search(mail_regex, self._mail)
            self.MAIL_USE_SSL = (regex.group(1).lower() == 'ssl')
            self.MAIL_USE_TLS = not self.MAIL_USE_SSL
            self.MAIL_SERVER = regex.group(4)
            self.MAIL_PORT = int(regex.group(5))
            self.MAIL_USERNAME = regex.group(2)
            self.MAIL_PASSWORD = regex.group(3)
            self.MAIL_DEFAULT_SENDER = 'Admin <{}>'.format(self.MAIL_USERNAME)

        # Make sure PROJECT_CONFIG is set
        Config._health_check()

    @staticmethod
    def _health_check():
        project_config = '{}_CONFIG'.format(project.__name__.upper())
        if not _getenv(project_config):
            raise Exception(
                'Environment variable {} is not set'.format(project_config)
            )


class DevConfig(Config):
    DEBUG = True

    # Settings for Flask-BasicAuth
    BASIC_AUTH_FORCE = False

    # Settings for Email by Flask-Mail
    _mail = _getenv('MAIL_DEV')

    # Settings for Database
    # If DATABASE_DEV is not available, use DATABASE_URL for Heroku support
    # If DATABASE_URL is not available neither, use local sqlite database
    SQLALCHEMY_DATABASE_URI = _getenv(
        'DATABASE_DEV',
        default=_getenv(
            'DATABASE_URL',
            default='sqlite:///{}_dev.sqlite3'.format(dirname(abspath(project.__file__)))
        )  # abspath is used for same behaviour of db migrate and run
    )

    # Settings for Redis
    BROKER_URL = _getenv('CELERY_BROKER_DEV')
    CELERY_RESULT_BACKEND = BROKER_URL


class TestConfig(Config):
    DEBUG = False

    # Settings for Flask-BasicAuth
    BASIC_AUTH_FORCE = True

    # Settings for Email by Flask-Mail
    _mail = _getenv('MAIL_TEST')

    # Settings for Database
    # If DATABASE_TEST is not available, use DATABASE_URL for Heroku support
    SQLALCHEMY_DATABASE_URI = _getenv(
        'DATABASE_TEST', default=_getenv('DATABASE_URL')
    )

    # Settings for Redis
    BROKER_URL = _getenv('CELERY_BROKER_TEST')
    CELERY_RESULT_BACKEND = BROKER_URL


class ProdConfig(Config):
    DEBUG = False

    # Settings for Flask-BasicAuth
    BASIC_AUTH_FORCE = True

    # Settings for Email by Flask-Mail
    _mail = _getenv('MAIL_PROD')

    # Settings for Database
    # If DATABASE_PROD is not available, use DATABASE_URL for Heroku support
    SQLALCHEMY_DATABASE_URI = _getenv(
        'DATABASE_PROD', default=_getenv('DATABASE_URL')
    )

    # Settings for Redis
    BROKER_URL = _getenv('CELERY_BROKER_PROD')
    CELERY_RESULT_BACKEND = BROKER_URL


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
