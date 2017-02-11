from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_mail import Mail
from easy_scheduler import Scheduler
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from werobot import WeRoBot
from celery import Celery
import arrow

bootstrap = Bootstrap()
db = SQLAlchemy()
httpauth = BasicAuth()
mail = Mail()
scheduler = Scheduler(timezone='Asia/Hong_Kong')
security = Security()
admin = Admin()
wechat = WeRoBot(enable_session=False)
worker = Celery()


def teardown(func):
    """Teardown works after initialization."""
    _app = None

    def wrapper(*args, **kwargs):
        global _app
        _app = func(*args, **kwargs)
        return _app
    return wrapper


@teardown
def create_app(cfg):
    """Create flask instance from configuration."""

    # Initialize flask instance.
    app = Flask(__name__)
    app.config.update(_upper(cfg.basic))

    # Initialize Flask-Bootstrap.
    _init_bootstrap(app, cfg)

    # Initialize Flask-SQLAlchemy.
    _init_db(app, cfg)

    # Initialize Flask-BasicAuth.
    _init_httpauth(app, cfg)

    # Initialize Flask-Mail
    _init_mail(app, cfg)

    # Initialize APScheduler.
    _init_scheduler(app, cfg)

    # Initialize Flask-Security.
    _init_auth(app, cfg)

    # Initialize Flask-Admin
    _init_admin(app, cfg)

    # Initialize index blueprint.
    _init_index(app, cfg)

    # Initialize wechat blueprint.
    _init_wechat(app, cfg)

    # Initialize Celery.
    _init_worker(app, cfg)

    return app


def _init_bootstrap(app, cfg):
    """Initialize Flask-Bootstrap."""
    if cfg.has_attr('bootstrap'):
        app.config.update(_upper(cfg.bootstrap))
        bootstrap.init_app(app)


def _init_db(app, cfg):
    """Initialize Flask-SQLAlchemy."""
    if cfg.has_attr('db'):
        app.config.update(_upper(cfg.db))
        db.init_app(app)

        import flask_boilerplate.models  # register tables

        # Initalize tables.
        with app.app_context():
            db.create_all()


def _init_httpauth(app, cfg):
    """Initialize Flask-BasicAuth."""
    if cfg.has_attr('httpauth'):
        app.config.update(_upper(cfg.httpauth))
        httpauth.init_app(app)


def _init_mail(app, cfg):
    """Initialize Flask-Mail."""
    if cfg.has_attr('mail'):
        app.config.update(_upper(cfg.mail))
        mail.init_app(app)


def _init_scheduler(app, cfg):
    """Initialize APScheduler."""
    if cfg.has_attr('scheduler'):
        scheduler.start()


def _init_auth(app, cfg):
    """Initialize Flask-Security."""
    if cfg.has_attr('auth'):
        app.config.update(_upper(cfg.auth))

        # Initialize datastore.
        from flask_boilerplate.models.user import User, Role

        _datastore = SQLAlchemyUserDatastore(db, User, Role)
        _security_ctx = security.init_app(app, _datastore)
        security.datastore = _datastore

        # Create default admins.
        with app.app_context():
            for email, pwd in cfg.auth['security_admins'].items():
                if not security.datastore.get_user(email):
                    security.datastore.create_user(
                        email=email, password=pwd,
                        confirmed_at=arrow.utcnow().datetime,
                    )
            security.datastore.commit()

        # Set Sending mail asynchronously via Celery.
        if cfg.auth['security_async_mail']:
            from flask_boilerplate.async.mail import send_mail

            _security_ctx.send_mail_task(lambda msg: send_mail.delay(
                subject=msg.subject, sender=msg.sender,
                recipients=msg.recipients, body=msg.body, html=msg.html
            ))

        from flask_admin import helpers as admin_helpers
        from flask import url_for
        @_security_ctx.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template,
                admin_view=admin.index_view,
                h=admin_helpers,
                get_url=url_for,
            )


def _init_admin(app, cfg):
    """Initialize Flask-Admin."""

    admin.template_mode = 'bootstrap3'
    admin.name = 'Admin'
    admin.base_template = 'admin/_admin_base.html'

    admin.init_app(app)

    from flask_boilerplate.models.user import User
    from flask_boilerplate.views.admin import UserView
    admin.add_view(UserView(User, db.session))


def _init_index(app, cfg):
    """Initialize index blueprint."""
    if cfg.has_attr('index'):
        from flask_boilerplate.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=cfg.index['index_blueprint_prefix'])


def _init_wechat(app, cfg):
    """Initialize wechat blueprint."""
    if cfg.has_attr('wechat'):
        wechat.config['TOKEN'] = cfg.wechat['wechat_token']
        wechat.config['SESSION_STORAGE'] = cfg.wechat['wechat_session_storage']

        import flask_boilerplate.views.wechat.views  # load robot handlers
        from werobot.contrib.flask import make_view
        app.add_url_rule(rule=cfg.wechat['wechat_view_route'],
                         endpoint='werobot',
                         view_func=make_view(wechat),
                         methods=['GET', 'POST'])


def _init_worker(app, cfg):
    """Initialize Celery."""
    worker.conf.update(cfg.celery)
    worker.main = __name__

    # Push context to Celery.
    worker.app = app
    TaskBase = worker.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with worker.app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    worker.Task = ContextTask

    # Register Celery tasks.
    import flask_boilerplate.async


def _upper(d):
    """Return non-lower dictionary from dictonary."""
    return dict(((k, d[k]) for k in d if k.isupper()))
