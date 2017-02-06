import unittest
from config import Config, DBConfig, WechatBlueprintConfig, CeleryConfig
from flask_template import create_app
from flask import render_template


class TestBasicConfig(unittest.TestCase):
    """Test basic configuration."""

    def test_basic_config(self):
        """Test BasicConfig class."""
        config = Config()
        self.assertTrue(config.has_attr('basic'))

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
        config = Config()
        self.assertFalse(config.has_attr('bootstrap'))

        config = Config(bootstrap=False)
        self.assertFalse(config.has_attr('bootstrap'))

        config = Config(bootstrap=True)
        self.assertTrue(config.has_attr('bootstrap'))

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
        config = Config()
        self.assertFalse(config.has_attr('db'))

        config = Config(db=False)
        self.assertFalse(config.has_attr('db'))

        config = Config(db=True)
        self.assertTrue(config.has_attr('db'))

    def test_database_config_in_app(self):
        """Test database configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
            app.config['SQLALCHEMY_DATABASE_URI']

        app = create_app(Config(db=False))
        with self.assertRaises(KeyError):
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
            app.config['SQLALCHEMY_DATABASE_URI']

        app = create_app(Config(db=True))
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
        app.config['SQLALCHEMY_DATABASE_URI']


class TestSchedulerConfig(unittest.TestCase):
    """Test scheduler configuration."""

    def test_scheduler_config(self):
        """Test SchedulerConfig class."""
        config = Config()
        self.assertFalse(config.has_attr('scheduler'))

        config = Config(scheduler=False)
        self.assertFalse(config.has_attr('scheduler'))

        config = Config(scheduler=True)
        self.assertTrue(config.has_attr('scheduler'))

    def test_scheduler(self):
        """Test scheduler in flask app."""
        create_app(Config())
        from flask_template import scheduler
        self.assertFalse(scheduler._scheduler.running)

        create_app(Config(scheduler=True))
        from flask_template import scheduler
        self.assertTrue(scheduler._scheduler.running)


class TestMailConfig(unittest.TestCase):
    """Test mail configuration."""

    def test_mail_config(self):
        """Test MailConfig class."""
        config = Config()
        self.assertFalse(config.has_attr('mail'))

        config = Config(mail=False)
        self.assertFalse(config.has_attr('mail'))

        config = Config(mail=True)
        self.assertTrue(config.has_attr('mail'))

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
        from flask_template.backend.async_tasks.async_tasks import send_mail
        self.assertEqual(send_mail(subject='success', body='success',
                                   recipients=['jxltom@gmail.com']), 0)

    def test_async_mail(self):
        """Test async mail."""
        create_app(Config(mail=True))
        from flask_template.backend.async_tasks.async_tasks import send_mail
        send_mail.delay(subject='success', body='success',
                        recipients=['jxltom@gmail.com'])


class TestIndexBlueprintConfig(unittest.TestCase):
    """Test index blueprint configuration."""

    def test_index_blueprint_config(self):
        """Test IndexConfig class."""
        config = Config()
        self.assertFalse(config.has_attr('index'))

        config = Config(index=False)
        self.assertFalse(config.has_attr('index'))

        config = Config(index=True)
        self.assertTrue(config.has_attr('index'))

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


class TestLoginBlueprintConfig(unittest.TestCase):
    """Test login blueprint configuration."""

    def setUp(self):
        from config import LoginBlueprintConfig
        self.login_url = \
            LoginBlueprintConfig.login_blueprint_prefix + \
            LoginBlueprintConfig.login_view_route

    def test_login_blueprint_config(self):
        """Test LoginConfig class."""
        config = Config()
        self.assertFalse(config.has_attr('login'))

        config = Config(login=False)
        self.assertFalse(config.has_attr('login'))

        config = Config(login=True)
        self.assertTrue(config.has_attr('login'))
        self.assertTrue(config.has_attr('bootstrap'))

    def test_login_manager_boostrap_instance(self):
        """Test login manager instance."""
        create_app(Config(login=True))
        from flask_template import login_manager
        self.assertTrue(login_manager.login_view)
        self.assertTrue(login_manager.LOGIN_VIEW_ROUTE)
        self.assertTrue(login_manager.LOGIN_USERNAME)
        self.assertTrue(login_manager.LOGIN_PASSWORD)
        self.assertTrue(login_manager.REDIRECT_URL_ON_SUCCESS)

    def test_login_blueprint_config_in_app(self):
        """Test login blueprint configuration in flask app."""
        app = create_app(Config(login=True))
        with self.assertRaises(KeyError):
            app.config['login_username']
            app.config['login_password']
            app.config['login_blueprint_prefix']
            app.config['login_view_route']

    def test_login_blueprint_route(self):
        """Test login blueprint route."""
        app = create_app(Config())
        app = app.test_client()
        rv = app.get(self.login_url)
        self.assertEqual(rv.status_code, 404)

        app = create_app(Config(login=True))
        app = app.test_client()
        rv = app.get(self.login_url)
        self.assertEqual(rv.status_code, 200)


class TestWechatBlueprintConfig(unittest.TestCase):
    """Test wechat blueprint configuration."""

    def test_wechat_blueprint_config(self):
        """Test WechatConfig class."""
        config = Config()
        self.assertFalse(config.has_attr('wechat'))

        config = Config(wechat=False)
        self.assertFalse(config.has_attr('wechat'))

        config = Config(wechat=True)
        self.assertTrue(config.has_attr('wechat'))

    def test_robot_instance(self):
        """Test robot instance."""
        create_app(Config(wechat=True))
        from flask_template import robot
        self.assertTrue(robot.config['TOKEN'])
        self.assertTrue(robot.config['SESSION_STORAGE'] is
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
        from flask_template import robot
        self.assertTrue(robot._handlers['text'])


class TestCeleryConfig(unittest.TestCase):
    """Test celery configuration."""

    def test_celery_config(self):
        """Test CeleryConfig class."""
        app = create_app(Config())
        from flask_template import worker
        self.assertEqual(worker.conf['CELERY_TIMEZONE'],
                         CeleryConfig.CELERY_TIMEZONE)
        self.assertEqual(worker.conf['CELERY_ENABLE_UTC'],
                         CeleryConfig.CELERY_ENABLE_UTC)
        self.assertEqual(worker.conf['BROKER_URL'],
                         CeleryConfig.BROKER_URL)
        self.assertEqual(worker.conf['CELERY_RESULT_BACKEND'],
                         CeleryConfig.CELERY_RESULT_BACKEND)

        with self.assertRaises(KeyError):
            app.config['CELERY_TIMEZONE']
            app.config['CELERY_ENABLE_UTC']
            app.config['BROKER_URL']
            app.config['CELERY_RESULT_BACKEND']

        with self.assertRaises(AttributeError):
            app.config.celery

    def test_celery(self):
        """Test celery."""
        create_app(Config())
        from flask_template.backend.async_tasks.async_tasks import async_test
        self.assertTrue(async_test.delay(1, 2))
