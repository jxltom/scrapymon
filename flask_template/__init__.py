from flask import Flask

bootstrap = None
db = None
login_manager = None
scheduler = None
robot = None


def create_app(cfg):
    """Create flask instance."""
    # Initialize flask instance.
    app = Flask(__name__)
    app.config.update(_upper(cfg.basic))

    # Initialize Flask-Bootstrap.
    if getattr(cfg, 'bootstrap', None) is not None:
        app.config.update(_upper(cfg.bootstrap))

        from flask_bootstrap import Bootstrap
        global bootstrap
        bootstrap = Bootstrap(app)
    else:
        bootstrap = None

    # Initialize for Flask-SQLAlchemy.
    if getattr(cfg, 'db', None) is not None:
        app.config.update(_upper(cfg.db))

        from flask_sqlalchemy import SQLAlchemy
        global db
        db = SQLAlchemy(app)
    else:
        db = None

    # Initialize for APScheduler.
    if getattr(cfg, 'scheduler', None) is not None:
        app.config.update(_upper(cfg.scheduler))

        from easy_scheduler import Scheduler
        global scheduler
        scheduler = Scheduler(timezone='Asia/Hong_Kong')
        scheduler.start()
    else:
        if scheduler:
            scheduler.shutdown()
            scheduler = None

    # Initialize index blueprint.
    if getattr(cfg, 'index', None) is not None:
        app.config.update(_upper(cfg.index))

        from flask_template.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=cfg.index['index_blueprint_prefix'])

    # Initialize login blueprint.
    if getattr(cfg, 'login', None) is not None:
        app.config.from_object(_upper(cfg.login))

        from flask_login import LoginManager
        global login_manager
        login_manager = LoginManager(app)

        login_manager.login_view = 'login.log_in'
        login_manager.LOGIN_VIEW_ROUTE = cfg.login['login_view_route']
        login_manager.LOGIN_USERNAME = cfg.login['login_username']
        login_manager.LOGIN_PASSWORD = cfg.login['login_password']
        login_manager.REDIRECT_URL_ON_SUCCESS = \
            cfg.login['redirect_url_on_success']

        from flask_template.views.login import login as login_blueprint
        app.register_blueprint(
            login_blueprint, url_prefix=cfg.login['login_blueprint_prefix'])
    else:
        login_manager = None

    # Initialize wechat blueprint.
    if getattr(cfg, 'wechat', None) is not None:
        app.config.update(_upper(cfg.wechat))

        from werobot import WeRoBot
        from werobot.contrib.flask import make_view
        global robot
        robot = WeRoBot(
            token=cfg.wechat['wechat_token'],
            enable_session=cfg.wechat['wechat_enable_session'],
            session_storage=cfg.wechat['wechat_session_storage']
        )

        from flask_template.views.wechat.views import robot  # refresh robot
        app.add_url_rule(rule=cfg.wechat['wechat_view_route'],
                         endpoint='werobot',
                         view_func=make_view(robot),
                         methods=['GET', 'POST'])
    else:
        robot = None

    return app


def _upper(d):
    """Return non-lower dictionary from dictonary."""
    return dict(((k, d[k]) for k in d if k.isupper()))
