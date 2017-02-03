from flask import Flask

bootstrap = None
db = None
login_manager = None
scheduler = None


def create_app(cfg):
    """Create flask instance."""
    app = Flask(__name__)
    app.config.update(cfg.basic)

    # Initialize Flask-Bootstrap.
    if getattr(cfg, 'bootstrap', None) is not None:
        app.config.update(cfg.bootstrap)

        from flask_bootstrap import Bootstrap
        global bootstrap
        bootstrap = Bootstrap(app)
    else:
        bootstrap = None

    # Initialize for Flask-SQLAlchemy.
    if getattr(cfg, 'db', None) is not None:
        app.config.update(cfg.db)

        from flask_sqlalchemy import SQLAlchemy
        global db
        db = SQLAlchemy(app)
    else:
        db = None

    # Initialize for APScheduler.
    if getattr(cfg, 'scheduler', None) is not None:
        app.config.update(cfg.scheduler)

        from flask_template.kernel.scheduler.scheduler import Scheduler
        global scheduler
        scheduler = Scheduler()
        scheduler.start()
    else:
        if scheduler:
            scheduler.shutdown()
            scheduler = None

    # Initialize index blueprint.
    if getattr(cfg, 'index', None) is not None:
        app.config.update(cfg.index)

        from flask_template.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=cfg.index['INDEX_BLUEPRINT_PREFIX'])

    # Initialize login blueprint.
    if getattr(cfg, 'login', None) is not None:
        app.config.update(cfg.login)

        from flask_login import LoginManager
        global login_manager
        login_manager = LoginManager(app)
        login_manager.login_view = 'login.log_in'
        login_manager.LOGIN_VIEW_ROUTE = cfg.login['LOGIN_VIEW_ROUTE']

        from flask_template.views.login import login as login_blueprint
        app.register_blueprint(
            login_blueprint, url_prefix=cfg.login['LOGIN_BLUEPRINT_PREFIX'])
    else:
        login_manager = None

    # Initialize wechat blueprint.
    if getattr(cfg, 'wechat', None) is not None:
        app.config.update(cfg.wechat)

        from werobot.contrib.flask import make_view
        from flask_template.views.wechat.views import robot
        robot.config['TOKEN'] = cfg.wechat['WECHAT_TOKEN']
        robot.config['SESSION_STORAGE'] = cfg.wechat['WECHAT_SESSION_STORAGE']

        app.add_url_rule(rule=cfg.wechat['WECHAT_VIEW_ROUTE'],
                         endpoint=cfg.wechat['WECHAT_BLUEPRINT_NAME'],
                         view_func=make_view(robot),
                         methods=['GET', 'POST'])
    else:
        from flask_template.views.wechat.views import robot
        robot.config['TOKEN'] = None
        robot.config['SESSION_STORAGE'] = None

    return app
