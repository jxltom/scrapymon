from flask import Flask

bootstrap, db, login_manager = None, None, None


def create_app(config):

    # create flask instance
    app = Flask(__name__)
    app.config.from_object(config)

    # register index view
    from flask_template.views.index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    # config for bootstrap
    if config.ENABLE_BOOTSTRAP:
        from flask_bootstrap import Bootstrap
        global bootstrap
        bootstrap = Bootstrap()
        bootstrap.init_app(app)

    # config for database
    if config.ENABLE_DATABASE:
        from flask_sqlalchemy import SQLAlchemy
        global db
        db = SQLAlchemy()
        db.init_app(app)

    # config for login view
    if config.ENABLE_LOGIN:
        from flask_login import LoginManager
        global login_manager
        login_manager = LoginManager()
        login_manager.init_app(app)

        from flask_template.views.login import login as login_blueprint
        app.register_blueprint(login_blueprint)

    return app
