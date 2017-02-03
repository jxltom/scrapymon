import unittest
from config import Config
from flask_template import create_app


class TestWechatBlueprint(unittest.TestCase):
    """Test wechat blueprint."""

    def setUp(self):
        self.wechat_url = '/wechat/'
        self.app = create_app(Config(wechat=True))

    def test_wechat(self):
        """Test wechat views."""
        app = self.app.test_client()
        app.post(self.wechat_url)
