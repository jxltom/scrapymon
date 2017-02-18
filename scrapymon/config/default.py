import os


class BasicConfig:
    """Configuration for flask instance."""
    SECRET_KEY = os.urandom(24)
    DEBUG = False


class BootstrapConfig:
    """Configuration for Flask-Bootstrap."""
    BOOTSTRAP_SERVE_LOCAL = True

    BOOTSTRAP_ENABLED = True  # used in template


class DBConfig:
    """Configuration for Flask-SQLAlchemy."""
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # The format of MySQL database URI can be
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' \
    #                           '<username>:<password>@<server>:3306/<database>'
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')


class HttpAuthConfig:
    """Configuration for Flask-BasicAuth."""
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = 'admin'
    BASIC_AUTH_FORCE = True


class MailConfig:
    """Configuration for Flask-Mail."""
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True if os.environ.get('MAIL_USE_TLS') == 'True' else False
    MAIL_USE_SSL = True if os.environ.get('MAIL_USE_SSL') == 'True' else False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class SchedulerConfig:
    """Configuration for APScheduler."""


class AuthConfig:
    """Configuration for Flask-Security."""
    SESSION_PROTECTION = 'strong'

    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = os.urandom(24)

    SECURITY_URL_PREFIX = '/admin'  # null for non-prefix
    SECURITY_LOGIN_URL = '/login'

    SECURITY_POST_LOGIN_VIEW = '/admin'
    SECURITY_POST_LOGOUT_VIEW = 'security.login'
    SECURITY_POST_REGISTER_VIEW = 'security.login'
    SECURITY_POST_CONFIRM_VIEW = 'security.login'
    SECURITY_POST_RESET_VIEW = 'security.login'
    SECURITY_POST_CHANGE_VIEW = 'security.change_password'
    SECURITY_UNAUTHORIZED_VIEW = 'security.login'

    SECURITY_CONFIRMABLE = True   # better as same as recoverable
    SECURITY_REGISTERABLE = False  # valid mail required
    SECURITY_RECOVERABLE = True  # valid mail required
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True

    SECURITY_DEFAULT_REMEMBER_ME = True

    security_async_mail = True
    security_admins = {
        'admin@example.tld': 'admin',
    }


class AdminConfig:
    """Configuration for Flask-Admin."""
    ADMIN_ENABLED = True

    FLASK_ADMIN_SWATCH = 'default'

    admin_template_mode = 'bootstrap3'
    admin_name = 'Admin'
    admin_base_template = 'admin/_base.html'


class IndexBlueprintConfig:
    """Configuration for index blueprint."""
    index_blueprint_prefix = None  # null for non-prefix

    # SCRAPYD_SERVER = 'http://jxltom.me:6800'
    SCRAPYD_SERVER = 'http://127.0.0.1:6800'


class WechatBlueprintConfig:
    """Configuration for werobot and wechat blueprint."""
    wechat_session_storage = None
    wechat_view_route = '/wechat/'  # ends with slash
    wechat_token = 'admin'


class CeleryConfig:
    """Configuration for Celery."""
    timezone = 'Asia/Hong_kong'
    enable_utc = True

    # A redis url can be
    # redis://:<password>@<server>:6379/0
    broker_url = os.environ.get('BROKER_URL')
    result_backend = os.environ.get('RESULT_BACKEND')


class Config:
    """Flask configuration."""

    __slots__ = ('basic', 'bootstrap', 'db', 'httpauth', 'mail', 'scheduler',
                 'auth', 'admin', 'index', 'wechat', 'celery')

    def __init__(self, **kwargs):
        """Initialize configuration.

        :param kwargs: boostrap, db, httpauth, mail, scheduler, auth, admin,
        index, wechat.
        """

        # Basic configuration for Flask.
        self.basic = self._dict_from_obj(BasicConfig)

        # Configuration for Flask-Bootstrap.
        if kwargs.get('bootstrap', None):
            self.bootstrap = self._dict_from_obj(BootstrapConfig)

        # Configuration for Flask-SQLAlchemy.
        if kwargs.get('db', None):
            self.db = self._dict_from_obj(DBConfig)

        # Configuration for Flask-BasicAuth.
        if kwargs.get('httpauth', None):
            self.httpauth = self._dict_from_obj(HttpAuthConfig)

        # Configuration for Flask-Mail.
        if kwargs.get('mail', None):
            self.mail = self._dict_from_obj(MailConfig)

        # Configuration for APScheduler.
        if kwargs.get('scheduler', None):
            self.scheduler = self._dict_from_obj(SchedulerConfig)

        # Configuration for Flask-Security.
        if kwargs.get('auth', None):
            self.bootstrap = self._dict_from_obj(BootstrapConfig)
            self.db = self._dict_from_obj(DBConfig)
            self.mail = self._dict_from_obj(MailConfig)
            self.auth = self._dict_from_obj(AuthConfig)

        # Configuration for Flask-Admin.
        if kwargs.get('admin', None):
            self.bootstrap = self._dict_from_obj(BootstrapConfig)
            self.db = self._dict_from_obj(DBConfig)
            self.mail = self._dict_from_obj(MailConfig)
            self.auth = self._dict_from_obj(AuthConfig)
            self.admin = self._dict_from_obj(AdminConfig)

        # Configuration for index blueprint.
        if kwargs.get('index', None):
            self.index = self._dict_from_obj(IndexBlueprintConfig)

        # Configuration for werobot and wechat blueprint.
        if kwargs.get('wechat', None):
            self.wechat = self._dict_from_obj(WechatBlueprintConfig)

        # Configuration for Celery.
        self.celery = self._dict_from_obj(CeleryConfig)

    @staticmethod
    def _dict_from_obj(obj):
        """Return dictionary from class for configuration."""
        return dict(((k, getattr(obj, k)) for k in dir(obj)))

    def has_attr(self, attr):
        """Check attribute existence."""
        if getattr(self, attr, None) is not None:
            return True
        return False
