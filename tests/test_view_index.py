from wsgi import app
import unittest


class TestViewIndex(unittest.TestCase):
    """This is for test the index module of views."""
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        pass
