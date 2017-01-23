import unittest
from config import Config
from flask_template import create_app


class TestWechatBlueprint(unittest.TestCase):
    """Test the wechat blueprint."""

    def setUp(self):
        config = Config()
        config.enable_wechat_blueprint()
        self.wechat_url = '/wechat/'
        self.app = create_app(config)

    def test_wechat(self):
        """Test wechat views."""
        app = self.app.test_client()
        with self.assertRaises(FileNotFoundError):
            app.post(self.wechat_url)
