from run import app
import unittest


class TestIndex(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        pass
