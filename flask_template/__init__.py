from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from easy_scheduler import Scheduler
from flask_mail import Mail
from flask_login import LoginManager
from werobot import WeRoBot
from celery import Celery

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
scheduler = Scheduler(timezone='Asia/Hong_Kong')
login_manager = LoginManager()
robot = WeRoBot(enable_session=False)
worker = Celery(__name__)

def teardown(func):

    def wrapper(*args, **kwargs):
        _app = func(*args, **kwargs)

        # Add context to Celery.
        TaskBase = worker.Task
        class ContextTask(TaskBase):
            abstract = True
            def __call__(self, *args, **kwargs):
                #with _app.app_context():
                _app.app_context.push()
                return TaskBase.__call__(self, *args, **kwargs)
        worker.Task = ContextTask

        # Register Celery tasks.
        from flask_template.backend.async_tasks import async_tasks

        return _app

    return wrapper


@teardown
def create_app(config):
    """Create flask instance."""

    # Initialize flask instance.
    app = Flask(__name__)
    app.config.update(_upper(config.basic))

    # Initialize Flask-Bootstrap.
    if config.has_attr('bootstrap'):
        app.config.update(_upper(config.bootstrap))
        bootstrap.init_app(app)

    # Initialize Flask-SQLAlchemy.
    if config.has_attr('db'):
        app.config.update(_upper(config.db))
        db.init_app(app)

        import flask_template.models  # load db tables

    # Initialize Flask-Mail
    if config.has_attr('mail'):
        app.config.update(_upper(config.mail))
        mail.init_app(app)

    # Initialize APScheduler.
    if config.has_attr('scheduler'):
        scheduler.start()

    # Initialize index blueprint.
    if config.has_attr('index'):
        from flask_template.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=config.index['index_blueprint_prefix'])

    # Initialize login blueprint.
    if config.has_attr('login'):
        login_manager.init_app(app)
        login_manager.login_view = 'login.log_in'
        login_manager.LOGIN_VIEW_ROUTE = config.login['login_view_route']
        login_manager.LOGIN_USERNAME = config.login['login_username']
        login_manager.LOGIN_PASSWORD = config.login['login_password']
        login_manager.REDIRECT_URL_ON_SUCCESS = \
            config.login['redirect_url_on_success']

        from flask_template.views.login import login as login_blueprint
        app.register_blueprint(
            login_blueprint, url_prefix=config.login['login_blueprint_prefix'])

    # Initialize wechat blueprint.
    if config.has_attr('wechat'):
        robot.config['TOKEN'] = config.wechat['wechat_token']
        robot.config['SESSION_STORAGE'] = config.wechat['wechat_session_storage']

        import flask_template.views.wechat.views  # load robot handlers
        from werobot.contrib.flask import make_view
        app.add_url_rule(rule=config.wechat['wechat_view_route'],
                         endpoint='werobot',
                         view_func=make_view(robot),
                         methods=['GET', 'POST'])

    # Initialize Celery.
    worker.conf.update(config.celery)

    return app


def _upper(d):
    """Return non-lower dictionary from dictonary."""
    return dict(((k, d[k]) for k in d if k.isupper()))
