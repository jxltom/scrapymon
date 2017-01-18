from wsgi import app
import unittest


class TestIndexBlueprint(unittest.TestCase):
    """Test the index blueprint."""
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        pass
