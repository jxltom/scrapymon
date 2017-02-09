from flask import Flask
from flask_bootstrap import Bootstrap
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from easy_scheduler import Scheduler
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager
from werobot import WeRoBot
from celery import Celery

bootstrap = Bootstrap()
db = SQLAlchemy()
basicauth = BasicAuth()
mail = Mail()
scheduler = Scheduler(timezone='Asia/Hong_Kong')
security = Security()
login_manager = LoginManager()
wechat = WeRoBot(enable_session=False)
worker = Celery()


def _teardown(func):
    """Teardown works after initialization."""
    _app = None

    def wrapper(*args, **kwargs):

        # Initialize flask instance.
        global _app
        _app = func(*args, **kwargs)

        # Register database tables
        if _app.extensions.get('sqlalchemy'):
            import flask_boilerplate.models
            with _app.app_context():
                db.create_all()

        # Initialize admin accounts for login
        #if getattr(_app, 'login_manager', None):
         #   from flask_boilerplate.models.user import User
         #   with _app.app_context():
          #      for uid, pwd in login_manager.login_admins.items():
          #          if not User.query.get(uid):
          #              db.session.add(User(uid, pwd))
          #      db.session.commit()

        # Push context to Celery.
        TaskBase = worker.Task
        class ContextTask(TaskBase):
            abstract = True
            def __call__(self, *args, **kwargs):
                with _app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
        worker.Task = ContextTask

        # Register Celery tasks (must load at last).
        import flask_boilerplate.async

        return _app
    return wrapper


def _upper(d):
    """Return non-lower dictionary from dictonary."""
    return dict(((k, d[k]) for k in d if k.isupper()))


@_teardown
def create_app(cfg):
    """Create flask instance."""

    # Initialize flask instance.
    app = Flask(__name__)
    app.config.update(_upper(cfg.basic))

    # Initialize Flask-Bootstrap.
    if cfg.has_attr('bootstrap'):
        app.config.update(_upper(cfg.bootstrap))
        bootstrap.init_app(app)

    # Initialize Flask-SQLAlchemy.
    if cfg.has_attr('db'):
        app.config.update(_upper(cfg.db))
        db.init_app(app)

    # Initialize Flask-BasicAuth.
    if cfg.has_attr('basicauth'):
        app.config.update(_upper(cfg.basicauth))
        basicauth.init_app(app)

    # Initialize Flask-Mail
    if cfg.has_attr('mail'):
        app.config.update(_upper(cfg.mail))
        mail.init_app(app)

    # Initialize APScheduler.
    if cfg.has_attr('scheduler'):
        scheduler.start()

    # Initialize index blueprint.
    if cfg.has_attr('index'):
        from flask_boilerplate.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=cfg.index['index_blueprint_prefix'])

    # Initialize login blueprint.
    if cfg.has_attr('login'):
        app.config.update(_upper(cfg.login))

        login_manager.init_app(app)
        login_manager.login_view = 'login.log_in'  # login view function
        login_manager.login_view_route = cfg.login['login_view_route']
        login_manager.success_redirect_url = cfg.login['success_redirect_url']
        login_manager.login_admins = cfg.login['login_admins']

        from flask_boilerplate.views.login import login as login_blueprint
        app.register_blueprint(
            login_blueprint, url_prefix=cfg.login['login_blueprint_prefix'])

    # Initialize wechat blueprint.
    if cfg.has_attr('wechat'):
        wechat.config['TOKEN'] = cfg.wechat['wechat_token']
        wechat.config['SESSION_STORAGE'] = cfg.wechat['wechat_session_storage']

        import flask_boilerplate.views.wechat.views  # load robot handlers
        from werobot.contrib.flask import make_view
        app.add_url_rule(rule=cfg.wechat['wechat_view_route'],
                         endpoint='werobot',
                         view_func=make_view(wechat),
                         methods=['GET', 'POST'])

    from flask_boilerplate.models.user import User, Role
    app.config['SECURITY_CONFIRMABLE'] = True
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_RECOVERABLE'] = True
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore)

    @security.send_mail_task
    def test(x):
        print('sd')
        return x

    # Initialize Celery.
    worker.conf.update(cfg.celery)
    worker.main = __name__

    return app
