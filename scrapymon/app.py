from flask import Flask
from flask_bootstrap import Bootstrap
from flask_basicauth import BasicAuth

bootstrap = Bootstrap()
httpauth = BasicAuth()


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

    # Initialize Flask-BasicAuth.
    _init_httpauth(app, cfg)

    # Initialize index blueprint.
    _init_index(app, cfg)

    return app


def _init_bootstrap(app, cfg):
    """Initialize Flask-Bootstrap."""
    if cfg.has_attr('bootstrap'):
        app.config.update(_upper(cfg.bootstrap))
        bootstrap.init_app(app)


def _init_httpauth(app, cfg):
    """Initialize Flask-BasicAuth."""
    if cfg.has_attr('httpauth'):
        app.config.update(_upper(cfg.httpauth))
        httpauth.init_app(app)


def _init_index(app, cfg):
    """Initialize index blueprint."""
    if cfg.has_attr('index'):
        app.config.update(_upper(cfg.index))

        from scrapymon.views.index import index as index_blueprint
        app.register_blueprint(
            index_blueprint, url_prefix=cfg.index['index_blueprint_prefix'])


def _upper(d):
    """Return non-lower dictionary from dictonary."""
    return dict(((k, d[k]) for k in d if k.isupper()))
