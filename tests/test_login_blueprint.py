import unittest
from config import Config
from flask_template import create_app


class TestLoginBlueprint(unittest.TestCase):
    """Test the login blueprint."""

    def setUp(self):
        """Initialize flask app."""
        cfg = Config(login=True)
        self.login_url = cfg.login['LOGIN_BLUEPRINT_PREFIX'] + \
                         cfg.login['LOGIN_VIEW_ROUTE']
        self.login_required_url = cfg.login['LOGIN_BLUEPRINT_PREFIX'] + \
                                  cfg.login['LOGIN_VIEW_ROUTE'] + \
                                  'login_required'
        self.app = create_app(cfg)
        self.app.config['LOGIN_USERNAME'] = 'admin'
        self.app.config['LOGIN_PASSWORD'] = 'admin'

    def test_login(self):
        """Test login blueprint."""
        app = self.app.test_client()
        rv = app.post(self.login_url,
                      data=dict(username='admin', password='admin',
                                remember=False, submit=True),
                      follow_redirects=False)
        self.assertTrue(rv.status_code in (200, 302))

        app = self.app.test_client()
        rv = app.post(self.login_url,
                      data=dict(username='admin', password='wrong'),
                      follow_redirects=False)
        self.assertTrue(rv.status_code in (200, 302))

    def test_login_required(self):
        """Test login required function."""
        app = self.app.test_client()
        rv = app.get(self.login_required_url)
        self.assertTrue('Unauthorized' not in rv.get_data(as_text=True))
        self.assertEqual(rv.status_code, 302)
