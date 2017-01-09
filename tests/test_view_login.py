import unittest
from config import Config
from flask_template import create_app


class TestViewLogin(unittest.TestCase):
    """Test the login view module."""

    def setUp(self):
        config = Config()
        config.enable_login_view()
        self.app = create_app(config)
        self.app.config['LOGIN_USERNAME'] = 'admin'
        self.app.config['LOGIN_PASSWORD'] = 'admin'

    def test_login(self):
        """It is hard to test since the CSRF check."""
        app = self.app.test_client()
        app.post(
            '/login',
            data=dict(username='admin', password='admin', remember=False, submit=True),
            follow_redirects=False)

        app = self.app.test_client()
        app.post(
            '/login',
            data=dict(username='admin', password='wrong'),
            follow_redirects=False)
