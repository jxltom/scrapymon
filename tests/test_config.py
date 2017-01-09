import unittest
from config import Config
from flask_template import create_app


class TestConfig(unittest.TestCase):
    """Test the config.py."""

    def test_bootstrap_config(self):
        config = Config()
        self.assertEqual(config.ENABLE_BOOTSTRAP, False)
        config = Config(bootstrap=True)
        self.assertEqual(config.ENABLE_BOOTSTRAP, True)
        config = Config(bootstrap=False)
        self.assertEqual(config.ENABLE_BOOTSTRAP, False)

    def test_bootstrap(self):
        self.assertTrue(bootstrap is not None)

    def test_database(self):
        'mysql+mysqlconnector://username:password@ip:port/database'
        pass


