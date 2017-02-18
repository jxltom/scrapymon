import unittest

from flask import render_template

from scrapymon.config import Config
from scrapymon.app import create_app


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
            app.config['BOOTSTRAP_ENABLED']

        app = create_app(Config(bootstrap=False))
        with self.assertRaises(KeyError):
            app.config['BOOTSTRAP_SERVE_LOCAL']
            app.config['BOOTSTRAP_ENABLED']

        app = create_app(Config(bootstrap=True))
        self.assertTrue(app.config['BOOTSTRAP_SERVE_LOCAL'])
        self.assertTrue(app.config['BOOTSTRAP_ENABLED'])

    def test_bootstrap_template(self):
        """Test base.html template when bootstrap not exists."""
        app = create_app(Config())
        with app.app_context():
            self.assertEqual(render_template('base.html'), '')

        app = create_app(Config(bootstrap=True))
        with app.app_context():
            with self.assertRaises(RuntimeError):
                render_template('base.html')


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
        rv = app.get('/_')
        self.assertEqual(rv.status_code, 200)

        app = create_app(Config(index=True, httpauth=True))
        app = app.test_client()
        rv = app.get('/_')
        self.assertEqual(rv.status_code, 401)


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
        self.assertEqual(rv.get_data(as_text=True), '')
