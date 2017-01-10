import unittest
from config import Config
from flask_template import create_app
from flask import render_template


class TestConfig(unittest.TestCase):
    """Test the basic parts of config.py."""

    def test_basic_config(self):
        """Test the basic configuration of flask."""
        app = create_app(Config())
        self.assertTrue(app.config['SECRET_KEY'])

    def test_debug_config(self):
        """Test the debug configuration of flask."""
        app = create_app(Config())
        self.assertTrue(app.config['DEBUG'])

        config = Config(debug=False)
        app = create_app(config)
        self.assertFalse(app.config['DEBUG'])


class TestBootstrapConfig(unittest.TestCase):
    """Test bootstrap in config.py."""

    def test_bootstrap_config(self):
        """Test the Config class."""
        config = Config()
        self.assertEqual(config.ENABLE_BOOTSTRAP, True)
        config = Config(bootstrap=True)
        self.assertEqual(config.ENABLE_BOOTSTRAP, True)
        config = Config(bootstrap=False)
        self.assertEqual(config.ENABLE_BOOTSTRAP, False)

    def test_bootstrap_instance(self):
        """Test the bootstrap instance in flask_template."""
        create_app(Config())
        from flask_template import bootstrap
        self.assertTrue(bootstrap is not None)

        create_app(Config(bootstrap=False))
        from flask_template import bootstrap
        self.assertTrue(bootstrap is None)

    def test_bootstrap_config_in_app(self):
        """Test the bootstrap configuration in flask app."""
        app = create_app(Config())
        self.assertEqual(app.config['ENABLE_BOOTSTRAP'], True)

        app = create_app(Config(bootstrap=False))
        self.assertEqual(app.config['ENABLE_BOOTSTRAP'], False)
        with self.assertRaises(KeyError):
            app.config['BOOTSTRAP_SERVE_LOCAL']

    def test_bootstrap_template(self):
        """Test the base.html template when bootstrap not exists."""
        app = create_app(Config(bootstrap=False))
        with app.app_context():
            self.assertEqual(render_template('base.html'), '')

        app = create_app(Config())
        with app.app_context():
            with self.assertRaises(RuntimeError):
                render_template('base.html')


class TestDatabaseConfig(unittest.TestCase):
    """Test database in config.py."""

    def test_database(self):
        'mysql+mysqlconnector://username:password@ip:port/database'
        pass


class TestLoginBlueprintConfig(unittest.TestCase):
    """Test login blueprint in config.py."""

    def test_login_blueprint_config(self):
        """Test login blueprint configuration."""
        app = create_app(Config())
        from flask_template import login_manager
        self.assertTrue(login_manager is None)
        self.assertFalse(app.config['ENABLE_LOGIN'])
        with self.assertRaises(KeyError):
            app.config['LOGIN_USERNAME']
            app.config['LOGIN_PASSWORD']
            app.config['LOGIN_BLUEPRINT_PREFIX']
            app.config['LOGIN_VIEW_ROUTE']

        config = Config()
        config.enable_login_view()
        app = create_app(config)
        self.assertEqual(app.config['ENABLE_BOOTSTRAP'], True)
        self.assertEqual(app.config['ENABLE_LOGIN'], True)
        self.assertTrue(app.config['LOGIN_USERNAME'])
        self.assertTrue(app.config['LOGIN_PASSWORD'])
        self.assertTrue(app.config['LOGIN_BLUEPRINT_PREFIX'])
        self.assertTrue(app.config['LOGIN_VIEW_ROUTE'])
        from flask_template import login_manager, bootstrap
        self.assertTrue(login_manager)
        self.assertTrue(login_manager.LOGIN_VIEW_ROUTE)
        self.assertTrue(bootstrap)

    def test_login_blueprint_enable(self):
        """Test enable and disable login blueprint."""
        app = create_app(Config())
        app = app.test_client()
        rv = app.get('/login')
        self.assertEqual(rv.status_code, 404)


class TestIndexBlueprintConfig(unittest.TestCase):
    """Test index blueprint in config.py."""

    def test_index_blueprint_config(self):
        """Test index blueprint module."""
        app = create_app(Config())
        self.assertFalse(app.config['ENABLE_INDEX'])
        with self.assertRaises(KeyError):
            app.config['INDEX_BLUEPRINT_PREFIX']

        config = Config()
        config.enable_index_view()
        app = create_app(config)
        self.assertTrue(app.config['ENABLE_INDEX'])
        self.assertTrue(app.config['INDEX_BLUEPRINT_PREFIX'])

    def test_index_blueprint_enable(self):
        """Test enable and disable login blueprint."""
        app = create_app(Config())
        app = app.test_client()
        rv = app.get('/')
        self.assertEqual(rv.status_code, 404)

        config = Config()
        config.enable_index_view()
        app = create_app(config)
        app = app.test_client()
        rv = app.get('/')
        self.assertEqual(rv.status_code, 200)

