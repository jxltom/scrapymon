from flask import Flask
from celery import Celery

bootstrap = None
db = None
login_manager = None
scheduler = None
robot = None
worker = Celery(__name__)


def create_app(config):
    """Create flask instance."""
    # Initialize flask instance.
    app = Flask(__name__)
    app.config.update(_upper(config.basic))

    # Initialize Celery
    worker.conf.update(config.celery)

    TaskBase = worker.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    worker.Task = ContextTask
    from flask_template.backend.celerytask import celerytask

    # Initialize Flask-Bootstrap.
    if getattr(config, 'bootstrap', None) is not None:
        app.config.update(_upper(config.bootstrap))

        from flask_bootstrap import Bootstrap
        global bootstrap
        bootstrap = Bootstrap(app)
    else:
        bootstrap = None

    # Initialize for Flask-SQLAlchemy.
    if getattr(config, 'db', None) is not None:
        app.config.update(_upper(config.db))

        from flask_sqlalchemy import SQLAlchemy
        global db
        db = SQLAlchemy(app)
    else:
        db = None

    # Initialize for APScheduler.
    if getattr(config, 'scheduler', None) is not None:
        app.config.update(_upper(config.scheduler))

        from easy_scheduler import Scheduler
        global scheduler
        scheduler = Scheduler(timezone='Asia/Hong_Kong')
        scheduler.start()
    else:
        if scheduler:
            scheduler.shutdown()
            scheduler = None

    # Initialize index blueprint.
    if getattr(config, 'index', None) is not None:
        app.config.update(_upper(config.index))

        from flask_template.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=config.index['index_blueprint_prefix'])

    # Initialize login blueprint.
    if getattr(config, 'login', None) is not None:
        app.config.from_object(_upper(config.login))

        from flask_login import LoginManager
        global login_manager
        login_manager = LoginManager(app)

        login_manager.login_view = 'login.log_in'
        login_manager.LOGIN_VIEW_ROUTE = config.login['login_view_route']
        login_manager.LOGIN_USERNAME = config.login['login_username']
        login_manager.LOGIN_PASSWORD = config.login['login_password']
        login_manager.REDIRECT_URL_ON_SUCCESS = \
            config.login['redirect_url_on_success']

        from flask_template.views.login import login as login_blueprint
        app.register_blueprint(
            login_blueprint, url_prefix=config.login['login_blueprint_prefix'])
    else:
        login_manager = None

    # Initialize wechat blueprint.
    if getattr(config, 'wechat', None) is not None:
        app.config.update(_upper(config.wechat))

        from werobot import WeRoBot
        from werobot.contrib.flask import make_view
        global robot
        robot = WeRoBot(
            token=config.wechat['wechat_token'],
            enable_session=config.wechat['wechat_enable_session'],
            session_storage=config.wechat['wechat_session_storage']
        )

        from flask_template.views.wechat.views import robot  # refresh robot
        app.add_url_rule(rule=config.wechat['wechat_view_route'],
                         endpoint='werobot',
                         view_func=make_view(robot),
                         methods=['GET', 'POST'])
    else:
        robot = None

    return app


def _upper(d):
    """Return non-lower dictionary from dictonary."""
    return dict(((k, d[k]) for k in d if k.isupper()))
