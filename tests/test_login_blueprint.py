import unittest
from config import Config, LoginBlueprintConfig
from flask_boilerplate import create_app


class TestLoginBlueprint(unittest.TestCase):
    """Test the login blueprint."""

    def setUp(self):
        """Initialize tests."""
        self.login_url = \
            LoginBlueprintConfig.login_blueprint_prefix + \
            LoginBlueprintConfig.login_view_route
        self.login_required_url = self.login_url + 'login_required'

        self.uid, self.pwd = list(LoginBlueprintConfig.login_admins.items())[0]

    def test_login(self):
        """Test login page."""
        app = create_app(Config(login=True))
        app = app.test_client()
        rv = app.post(
            self.login_url,
            data=dict(username=self.uid, password=self.pwd,
                      remember=False, submit=True),
            follow_redirects=False
        )
        self.assertTrue(rv.status_code in (200, 302))

        rv = app.post(
            self.login_url,
            data=dict(username='invalid', password='invalid'),
            follow_redirects=False
        )
        self.assertTrue(rv.status_code in (200, 302))

    def test_login_required(self):
        """Test required login page."""
        app = create_app(Config(login=True))
        app = app.test_client()
        rv = app.get(self.login_required_url)
        self.assertTrue('Unauthorized' not in rv.get_data(as_text=True))
        self.assertEqual(rv.status_code, 302)
