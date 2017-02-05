import unittest
from config import Config, CeleryConfig
from flask_template import create_app, create_worker
from flask import render_template


class TestBasicConfig(unittest.TestCase):
    """Test basic configuration in config.py."""

    def test_secrete_key(self):
        """Test secrete key of flask."""
        app = create_app(Config())
        self.assertTrue(app.config['SECRET_KEY'])

    def test_debug(self):
        """Test debug of flask."""
        app = create_app(Config())
        self.assertFalse(app.config['DEBUG'])

        app = create_app(Config())
        app.config.update(DEBUG=True)
        self.assertTrue(app.config['DEBUG'])


class TestBootstrapConfig(unittest.TestCase):
    """Test bootstrap configuration in config.py."""

    def test_bootstrap_config(self):
        """Test BootstrapConfig class."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.bootstrap

        cfg = Config(bootstrap=False)
        with self.assertRaises(AttributeError):
            cfg.bootstrap

        cfg = Config(bootstrap=True)
        self.assertTrue(cfg.bootstrap)

    def test_bootstrap_instance(self):
        """Test bootstrap instance in flask_template."""
        create_app(Config())
        from flask_template import bootstrap
        self.assertTrue(bootstrap is None)

        create_app(Config(bootstrap=False))
        from flask_template import bootstrap
        self.assertTrue(bootstrap is None)

        create_app(Config(bootstrap=True))
        from flask_template import bootstrap
        self.assertTrue(bootstrap is not None)

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
    """Test database in config.py."""

    def setUp(self):
        """Initialize test."""
        self.db = 'mysql+mysqlconnector://' \
                  'flask-template:flask-template' \
                  '@jxltom.me:3306/flask-template'

    def test_database_config(self):
        """Test DatabaseConfig class."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.db

        cfg = Config(db='')
        with self.assertRaises(AttributeError):
            cfg.db

        cfg = Config(db=False)
        with self.assertRaises(AttributeError):
            cfg.db

        cfg = Config(db=self.db)
        self.assertTrue(cfg.db)

    def test_database_instance(self):
        """Test db instance."""
        create_app(Config())
        from flask_template import db
        self.assertTrue(db is None)

        create_app(Config(db=''))
        from flask_template import db
        self.assertTrue(db is None)

        create_app(Config(db=self.db))
        from flask_template import db
        self.assertTrue(db)

    def test_database_config_in_app(self):
        """Test database configuration in flask app."""
        app = create_app(Config())
        with self.assertRaises(KeyError):
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
            app.config['SQLALCHEMY_DATABASE_URI']

        app = create_app(Config(db=''))
        with self.assertRaises(KeyError):
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
            app.config['SQLALCHEMY_DATABASE_URI']

        app = create_app(Config(db=self.db))
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
        app.config['SQLALCHEMY_DATABASE_URI']


class TestSchedulerConfig(unittest.TestCase):
    """Test scheduler configuration in config.py."""

    def test_scheduler_config(self):
        """Test SchedulerClass config."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.scheduler

        cfg = Config(scheduler=False)
        with self.assertRaises(AttributeError):
            cfg.scheduler

        cfg = Config(scheduler=True)
        self.assertTrue(type(cfg.scheduler) is dict)

    def test_scheduler_instance(self):
        """Test scheduelr instance."""
        create_app(Config())
        from flask_template import scheduler
        self.assertTrue(scheduler is None)

        create_app(Config(scheduler=False))
        from flask_template import scheduler
        self.assertTrue(scheduler is None)

        create_app(Config(scheduler=True))
        from flask_template import scheduler
        self.assertTrue(scheduler)


class TestMailConfig(unittest.TestCase):
    """Test mail in conf.py."""

    def test_mail_config(self):
        """Test MailConfig config."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.mail

        cfg = Config(mail=False)
        with self.assertRaises(AttributeError):
            cfg.mail

        cfg = Config(mail=True)
        self.assertTrue(cfg.mail)

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

    def test_mail_instance(self):
        """Test mail instance."""
        create_app(Config())
        from flask_template import mail
        self.assertTrue(mail is None)

        create_app(Config(mail=False))
        from flask_template import mail
        self.assertTrue(mail is None)

        create_app(Config(mail=True))
        from flask_template import mail
        self.assertTrue(mail)

    def test_mail(self):
        """Test mail."""
        from flask_template.backend.async_tasks.async_tasks import send_mail
        self.assertEqual(send_mail(subject='success', body='success',
                                   recipients=['jxltom@gmail.com']), 0)

    def test_async_mail(self):
        """Test async mail."""
        from flask_template.backend.async_tasks.async_tasks import send_mail
        send_mail.delay(subject='success', body='success',
                        recipients=['jxltom@gmail.com'])


class TestIndexBlueprintConfig(unittest.TestCase):
    """Test index blueprint in config.py."""

    def test_index_blueprint_config(self):
        """Test IndexConfig class."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.index

        cfg = Config(index=False)
        with self.assertRaises(AttributeError):
            cfg.index

        cfg = Config(index=True)
        self.assertTrue(cfg.index)

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
    """Test login blueprint in config.py."""

    def setUp(self):
        from config import LoginBlueprintConfig
        self.login_url = \
            LoginBlueprintConfig.login_blueprint_prefix + \
            LoginBlueprintConfig.login_view_route

    def test_login_blueprint_config(self):
        """Test LoginConfig class."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.login

        cfg = Config(login=False)
        with self.assertRaises(AttributeError):
            cfg.login

        cfg = Config(login=True)
        self.assertTrue(cfg.login)

    def test_login_manager_boostrap_instance(self):
        """Test login manager instance."""
        create_app(Config())
        from flask_template import login_manager
        self.assertTrue(login_manager is None)

        create_app(Config(login=False))
        from flask_template import login_manager
        self.assertTrue(login_manager is None)

        create_app(Config(login=True))
        from flask_template import login_manager, bootstrap
        self.assertTrue(login_manager is not None)
        self.assertTrue(login_manager.login_view)
        self.assertTrue(login_manager.LOGIN_VIEW_ROUTE)
        self.assertTrue(login_manager.LOGIN_USERNAME)
        self.assertTrue(login_manager.LOGIN_PASSWORD)
        self.assertTrue(login_manager.REDIRECT_URL_ON_SUCCESS)

        self.assertTrue(bootstrap)

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
    """Test wechat blueprint in config.py."""

    def test_wechat_blueprint_config(self):
        """Test WechatConfig class."""
        cfg = Config()
        with self.assertRaises(AttributeError):
            cfg.wechat

        cfg = Config(wechat=False)
        with self.assertRaises(AttributeError):
            cfg.wechat

        cfg = Config(wechat=True)
        self.assertTrue(cfg.wechat)

    def test_robot_instance(self):
        """Test robot instance."""
        create_app(Config())
        from flask_template import robot
        self.assertTrue(robot is None)

        create_app(Config(wechat=True))
        from flask_template import robot
        self.assertTrue(robot is not None)
        self.assertTrue(robot.config['TOKEN'])
        self.assertTrue(robot.config['SESSION_STORAGE'] is None)

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
    """Test celery configuration in config.py"""

    def test_celery_config(self):
        """Test CeleryConfig class."""
        app = create_app(Config())
        worker = create_worker(app)
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
        from flask_template.backend.async_tasks.async_tasks import async_test
        self.assertTrue(async_test.delay(1, 2))
