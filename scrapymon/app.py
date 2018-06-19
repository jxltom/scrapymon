import os
from os.path import dirname, join, abspath
import sys
import uuid

from flask import Flask
from flask.json import JSONEncoder
from flask_compress import Compress
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from flask_user import UserManager, SQLAlchemyAdapter
from flask_admin import Admin
from apscheduler.schedulers.background import BackgroundScheduler
from celery.__main__ import main as celery_main
from raven.contrib.flask import Sentry
from whitenoise import WhiteNoise
import click

import flask_boilerplate as project
from flask_boilerplate.settings import config


PROJECT_NAME = project.__name__
ENV_CONFIG = os.getenv('{}_CONFIG'.format(PROJECT_NAME.upper()), 'dev')

# TODO: ADD REST API support
sentry = Sentry()
compress = Compress()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()
usermanager = UserManager()
scheduler = BackgroundScheduler()


class CustomJSONEncoder(JSONEncoder):
    """Custom JSON output."""
    item_separator = ','
    key_separator = ':'

    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(CustomJSONEncoder, self).__init__(**kwargs)


def create_app():
    # Initialize Flask instance and enable static file serving
    app = Flask(__name__)
    app.config.from_object(config[ENV_CONFIG]())  # instance is for __init__
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

    # Initialize Sentry for error tracking
    sentry.init_app(app)

    # Custom Json
    app.json_encoder = CustomJSONEncoder
    compress.init_app(app)

    # Initialize DebugToolbar
    if app.config['DEBUG']:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)

    # Initialize Mail by Flask-Mail
    mail.init_app(app)

    # Initialize Database and Migration by Flask-Sqlalchey and Flask-Migrate
    db.init_app(app)
    migrate.init_app(
        app, db,
        directory=join(abspath(dirname(project.__file__)), 'migrations')
    )  # set directory for compatible with Heroku

    # Initialize Authentication by Flask-Login and Flask-User
    from .blueprints.user import User
    from .utils.mail import flaskuser_sendmail
    _adapter = SQLAlchemyAdapter(db, User)
    usermanager.init_app(app, _adapter, send_email_function=flaskuser_sendmail)

    # Initialize Administration by Flask-Admin
    from .blueprints.admin import (
        IndexView, UserModelView, RoleModelView
    )
    from .blueprints.user import User, Role
    admin = Admin(app=app, index_view=IndexView(), template_mode='bootstrap3')
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))

    # Initialize app blueprint
    from .blueprints.app import app as app_blueprint
    app.register_blueprint(app_blueprint, url_prefix='')

    # TODO: Can not run celeryworker if this is initialized
    # Initialize scheduler
    # Note the scheduler must be initialized before the jobs are imported
    # timezone = app.config.get('APSCHEDULER_TIMEZONE', None)
    # jobstores = app.config.get('APSCHEDULER_JOBSTORES', {})
    # executors = app.config.get('APSCHEDULER_EXECUTORS', {})
    # job_defaults = app.config.get('APSCHEDULER_JOB_DEFAULTS', {})
    # scheduler.configure(
    #     timezone=timezone,
    #     jobstores=jobstores, executors=executors, job_defaults=job_defaults
    # )

    # Initialize CLI shell command
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db, User=User, Role=Role)

    # Initialize CLI command for creating Superuser for authentication
    @app.cli.command()
    def createsuperuser():
        from .blueprints.user import User, Role
        Role.create_roles()
        User.create_superuser()

    # Initialize CLI command for populating fake Users
    @app.cli.command()
    def genfakedata():
        from .blueprints.user import User
        User.genfakeusers()

    # Initialize CLI command for Celery
    @app.cli.command()
    @click.argument('queue', nargs=1, default=PROJECT_NAME)
    def celeryworker(queue):
        sys.argv = [
            'celery', 'worker', '-n {}@%h'.format(uuid.uuid4()),
            '-A', '{}.celery_app:celery_application'.format(PROJECT_NAME), '-E',
            '-Q', queue,
            '--loglevel=info'
        ]
        sys.exit(celery_main())

    @app.cli.command()
    def celerybeat():
        sys.argv = [
            'celery', 'beat',
            '-A', '{}.celery_app:celery_application'.format(PROJECT_NAME),
            '--loglevel=info'
        ]
        sys.exit(celery_main())

    # Initialize CLI command for pytest-cov
    @app.cli.command(name='py.test')
    @click.option('--cov')
    @click.option('--cov-report')
    def pytest_cov(cov, cov_report):
        """Run pytest with pytest-cov plugin."""
        import pytest

        sys.argv = ['py.test', '-s']
        sys.argv += ['--cov={}'.format(cov)] if cov else []
        sys.argv += ['--cov-report={}'.format(cov_report)] if cov_report else []

        sys.exit(pytest.main())

    return app


application = create_app()
