import os


class BasicConfig:
    """Configuration for flask instance."""
    SECRET_KEY = os.urandom(24)
    DEBUG = False


class BootstrapConfig:
    """Configuration for Flask-Bootstrap."""
    BOOTSTRAP_SERVE_LOCAL = True

    BOOTSTRAP_ENABLED = True  # used in template


class HttpAuthConfig:
    """Configuration for Flask-BasicAuth."""
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = 'admin'
    BASIC_AUTH_FORCE = True


class IndexBlueprintConfig:
    """Configuration for index blueprint."""
    index_blueprint_prefix = None  # null for non-prefix

    # SCRAPYD_SERVER = 'http://jxltom.me:6800'
    SCRAPYD_SERVER = 'http://127.0.0.1:6800'


class Config:
    """Flask configuration."""

    __slots__ = ('basic', 'bootstrap', 'httpauth', 'index')

    def __init__(self, **kwargs):
        """Initialize configuration.

        :param kwargs: boostrap, httpauth, index.
        """

        # Basic configuration for Flask.
        self.basic = self._dict_from_obj(BasicConfig)

        # Configuration for Flask-Bootstrap.
        if kwargs.get('bootstrap', None):
            self.bootstrap = self._dict_from_obj(BootstrapConfig)

        # Configuration for Flask-BasicAuth.
        if kwargs.get('httpauth', None):
            self.httpauth = self._dict_from_obj(HttpAuthConfig)

        # Configuration for index blueprint.
        if kwargs.get('index', None):
            self.index = self._dict_from_obj(IndexBlueprintConfig)

    @staticmethod
    def _dict_from_obj(obj):
        """Return dictionary from class for configuration."""
        return dict(((k, getattr(obj, k)) for k in dir(obj)))

    def has_attr(self, attr):
        """Check attribute existence."""
        if getattr(self, attr, None) is not None:
            return True
        return False
