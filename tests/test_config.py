import unittest
from config import Config, DBConfig, WechatBlueprintConfig, CeleryConfig
from flask_boilerplate import create_app
from flask import render_template


class TestBasicConfig(unittest.TestCase):
    """Test basic configuration."""

    def test_basic_config(self):
        """Test BasicConfig class."""
        cfg = Config()
        self.assertTrue(cfg.has_attr('basic'))

    def test_basic_config_in_app(self):
        """Test basic configuration in flask app."""
        app = create_app(Config())
        self.assertTrue(app.config['SECRET_KEY'])
        self.assertFalse(app.config['DEBUG'])

        app = create_app(Config())
        app.config.update(DEBUG=True)
        self.assertTrue(app.config['DEBUG'])


class TestBootstrapConfig(unittest.TestCase):
    """Test bootstrap configuration."""

    def test_bootstrap_config(self):
        """Test BootstrapConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('bootstrap'))

        cfg = Config(bootstrap=False)
        self.assertFalse(cfg.has_attr('bootstrap'))

        cfg = Config(bootstrap=True)
        self.assertTrue(cfg.has_attr('bootstrap'))

    def test_bootstrap_config_in_app(self):
        """Test bootstrap configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['BOOTSTRAP_SERVE_LOCAL']
            app.config['BOOTSTRAP_USE_MINIFIED']

        app = create_app(Config(bootstrap=False))
        with self.assertRaises(KeyError):
            app.config['BOOTSTRAP_SERVE_LOCAL']
            app.config['BOOTSTRAP_USE_MINIFIED']

        app = create_app(Config(bootstrap=True))
        self.assertTrue(app.config['BOOTSTRAP_SERVE_LOCAL'])
        self.assertTrue(app.config['BOOTSTRAP_USE_MINIFIED'])

    def test_bootstrap_template(self):
        """Test base.html template when bootstrap not exists."""
        app = create_app(Config())
        with app.app_context():
            self.assertEqual(render_template('base.html'), '')

        app = create_app(Config(bootstrap=True))
        with app.app_context():
            with self.assertRaises(RuntimeError):
                render_template('base.html')


class TestDatabaseConfig(unittest.TestCase):
    """Test database configuration."""

    def setUp(self):
        """Initialize tests."""
        self.uri = DBConfig.SQLALCHEMY_DATABASE_URI

    def test_database_config(self):
        """Test DatabaseConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('db'))

        cfg = Config(db=False)
        self.assertFalse(cfg.has_attr('db'))

        cfg = Config(db=True)
        self.assertTrue(cfg.has_attr('db'))

    def test_database_config_in_app(self):
        """Test database configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
            app.config['SQLALCHEMY_DATABASE_URI']
            app.config['SQLALCHEMY_ECHO']

        app = create_app(Config(db=False))
        with self.assertRaises(KeyError):
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
            app.config['SQLALCHEMY_DATABASE_URI']
            app.config['SQLALCHEMY_ECHO']

        app = create_app(Config(db=True))
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
        app.config['SQLALCHEMY_DATABASE_URI']
        app.config['SQLALCHEMY_ECHO']


class TestHttpAuthConfig(unittest.TestCase):
    """Test http auth configuration."""

    def test_http_auth_config(self):
        """Test HttpAuthConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('httpauth'))

        cfg = Config(basicauth=False)
        self.assertFalse(cfg.has_attr('httpauth'))

        cfg = Config(httpauth=True)
        self.assertTrue(cfg.has_attr('httpauth'))

    def test_http_auth_config_in_app(self):
        """Test http auth configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['BASIC_AUTH_USERNAME']
            app.config['BASIC_AUTH_PASSWORD']
            app.config['BASIC_AUTH_FORCE']

        app = create_app(Config(httpauth=False))
        with self.assertRaises(KeyError):
            app.config['BASIC_AUTH_USERNAME']
            app.config['BASIC_AUTH_PASSWORD']
            app.config['BASIC_AUTH_FORCE']

        app = create_app(Config(httpauth=True))
        self.assertTrue(app.config['BASIC_AUTH_USERNAME'])
        self.assertTrue(app.config['BASIC_AUTH_PASSWORD'])
        self.assertTrue(app.config['BASIC_AUTH_FORCE'] in (True, False))

    def test_http_auth(self):
        """Test http auth."""
        app = create_app(Config(index=True))
        app = app.test_client()
        rv = app.get('_')
        self.assertEqual(rv.status_code, 200)

        app = create_app(Config(index=True, httpauth=True))
        app = app.test_client()
        rv = app.get('_')
        self.assertEqual(rv.status_code, 401)


class TestMailConfig(unittest.TestCase):
    """Test mail configuration."""

    def test_mail_config(self):
        """Test MailConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('mail'))

        cfg = Config(mail=False)
        self.assertFalse(cfg.has_attr('mail'))

        cfg = Config(mail=True)
        self.assertTrue(cfg.has_attr('mail'))

    def test_mail_config_in_app(self):
        """Test mail configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['MAIL_SERVER']
            app.config['MAIL_PORT']
            app.config['MAIL_USE_TLS']
            app.config['MAIL_USE_SSL']
            app.config['MAIL_USERNAME']
            app.config['MAIL_PASSWORD']
            app.config['MAIL_DEFAULT_SENDER']

        app = create_app(Config(mail=True))
        self.assertTrue(app.config['MAIL_SERVER'])
        self.assertTrue(app.config['MAIL_PORT'])
        self.assertTrue(app.config['MAIL_USE_TLS'] in (True, False))
        self.assertTrue(app.config['MAIL_USE_SSL'] in (True, False))
        self.assertTrue(app.config['MAIL_USERNAME'])
        self.assertTrue(app.config['MAIL_PASSWORD'])
        self.assertTrue(app.config['MAIL_DEFAULT_SENDER'] or
                        app.config['MAIL_DEFAULT_SENDER'] is None)

    def test_mail(self):
        """Test mail."""
        create_app(Config(mail=True))
        from flask_boilerplate.async.mail import send_mail
        self.assertEqual(send_mail(subject='success', body='success',
                                   recipients=['jxltom@gmail.com']), 0)

    def test_async_mail(self):
        """Test async mail."""
        create_app(Config(mail=True))
        from flask_boilerplate.async.mail import send_mail
        send_mail.delay(subject='success', body='success',
                        recipients=['jxltom@gmail.com'])


class TestSchedulerConfig(unittest.TestCase):
    """Test scheduler configuration."""

    def test_scheduler_config(self):
        """Test SchedulerConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('scheduler'))

        cfg = Config(scheduler=False)
        self.assertFalse(cfg.has_attr('scheduler'))

        cfg = Config(scheduler=True)
        self.assertTrue(cfg.has_attr('scheduler'))

    def test_scheduler(self):
        """Test scheduler in flask app."""
        create_app(Config())
        from flask_boilerplate import scheduler
        self.assertFalse(scheduler._scheduler.running)

        create_app(Config(scheduler=True))
        from flask_boilerplate import scheduler
        self.assertTrue(scheduler._scheduler.running)


class TestAuthConfig(unittest.TestCase):
    """Test auth configuration."""

    def test_auth_config(self):
        """Test SecurityConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('auth'))

        cfg = Config(auth=False)
        self.assertFalse(cfg.has_attr('auth'))

        cfg = Config(auth=True)
        self.assertTrue(cfg.has_attr('bootstrap'))
        self.assertTrue(cfg.has_attr('db'))
        self.assertTrue(cfg.has_attr('mail'))
        self.assertTrue(cfg.has_attr('auth'))
        self.assertEqual(type(cfg.auth['security_admins']), dict)

    def test_auth_config_in_app(self):
        """Test auth configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['SESSION_PROTECTION']

            app.config['SECURITY_PASSWORD_HASH']
            app.config['SECURITY_PASSWORD_SALT']

            app.config['SECURITY_URL_PREFIX']
            app.config['SECURITY_LOGIN_URL']

            app.config['SECURITY_POST_LOGIN_VIEW']
            app.config['SECURITY_POST_LOGOUT_VIEW']

            app.config['SECURITY_CONFIRMABLE']
            app.config['SECURITY_REGISTERABLE']
            app.config['SECURITY_RECOVERABLE']
            app.config['SECURITY_TRACKABLE']
            app.config['SECURITY_CHANGEABLE']

            app.config['security_async_mail']
            app.config['security_admins']

        app = create_app(Config(auth=True))
        self.assertTrue(app.config['SESSION_PROTECTION'])

        self.assertTrue(app.config['SECURITY_PASSWORD_HASH'])
        self.assertTrue(app.config['SECURITY_PASSWORD_SALT'])
        self.assertTrue(type(app.config['SECURITY_PASSWORD_SALT']) in (str, bytes))

        app.config['SECURITY_URL_PREFIX']
        app.config['SECURITY_LOGIN_URL']

        app.config['SECURITY_POST_LOGIN_VIEW']
        app.config['SECURITY_POST_LOGOUT_VIEW']

        app.config['SECURITY_CONFIRMABLE']
        app.config['SECURITY_REGISTERABLE']
        app.config['SECURITY_RECOVERABLE']
        app.config['SECURITY_TRACKABLE']
        app.config['SECURITY_CHANGEABLE']

        with self.assertRaises(KeyError):
            app.config['security_async_mail']
            app.config['security_admins']

    def test_auth(self):
        """Test auth."""
        app = create_app(Config(index=True, auth=True))
        app = app.test_client()
        rv = app.get('/_login_required')
        self.assertEqual(rv.status_code, 302)


class TestIndexBlueprintConfig(unittest.TestCase):
    """Test index blueprint configuration."""

    def test_index_blueprint_config(self):
        """Test IndexConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('index'))

        cfg = Config(index=False)
        self.assertFalse(cfg.has_attr('index'))

        cfg = Config(index=True)
        self.assertTrue(cfg.has_attr('index'))

    def test_index_blueprint_config_in_app(self):
        """Test index blueprint configuration in app."""
        app = create_app(Config(index=True))
        with self.assertRaises(KeyError):
            app.config['index_blueprint_prefix']

    def test_index_blueprint_route(self):
        """Test index blueprint route."""
        app = create_app(Config())
        app = app.test_client()
        rv = app.get('/_')
        self.assertEqual(rv.status_code, 404)

        app = create_app(Config(index=True))
        app = app.test_client()
        rv = app.get('/_')
        self.assertEqual(rv.get_data(as_text=True), 'success')


class TestWechatBlueprintConfig(unittest.TestCase):
    """Test wechat blueprint configuration."""

    def setUp(self):
        self.wechat_url = WechatBlueprintConfig.wechat_view_route

    def test_wechat_blueprint_config(self):
        """Test WechatConfig class."""
        cfg = Config()
        self.assertFalse(cfg.has_attr('wechat'))

        cfg = Config(wechat=False)
        self.assertFalse(cfg.has_attr('wechat'))

        cfg = Config(wechat=True)
        self.assertTrue(cfg.has_attr('wechat'))

    def test_robot_instance(self):
        """Test robot instance."""
        create_app(Config(wechat=True))
        from flask_boilerplate import wechat
        self.assertTrue(wechat.config['TOKEN'])
        self.assertTrue(wechat.config['SESSION_STORAGE'] is
                        WechatBlueprintConfig.wechat_session_storage)

    def test_wechat_blueprint_config_in_app(self):
        """Test wechat blueprint configurationin flask app."""
        app = create_app(Config(wechat=True))
        with self.assertRaises(KeyError):
            app.config['wechat_token']
            app.config['wechat_session_storage']
            app.config['wechat_blueprint_prefix']
            app.config['wechat_view_route']

    def test_wechat_blueprint_route(self):
        """Test wechat blueprint route."""
        create_app(Config(wechat=True))
        from flask_boilerplate import wechat
        self.assertTrue(wechat._handlers['text'])

    def test_wechat(self):
        """Test wechat views."""
        app = create_app(Config(wechat=True))
        app = app.test_client()
        rv = app.post(self.wechat_url)
        self.assertEqual(rv.status_code, 403)
        self.assertTrue('WeRoBot' in rv.get_data(as_text=True))

        rv = app.get(self.wechat_url)
        self.assertEqual(rv.status_code, 403)
        self.assertTrue('WeRoBot' in rv.get_data(as_text=True))


class TestCeleryConfig(unittest.TestCase):
    """Test celery configuration."""

    def test_celery_config(self):
        """Test CeleryConfig class."""
        app = create_app(Config())
        from flask_boilerplate import worker
        self.assertEqual(worker.conf['timezone'],
                         CeleryConfig.timezone)
        self.assertEqual(worker.conf['enable_utc'],
                         CeleryConfig.enable_utc)
        self.assertEqual(worker.conf['broker_url'],
                         CeleryConfig.broker_url)
        self.assertEqual(worker.conf['result_backend'],
                         CeleryConfig.result_backend)

        with self.assertRaises(KeyError):
            app.config['timezone']
            app.config['enable_utc']
            app.config['BROKER_URL']
            app.config['result_backend']

    def test_celery(self):
        """Test celery."""
        create_app(Config())
        from flask_boilerplate.async.mail import async_test
        self.assertTrue(async_test.delay(1, 2))
