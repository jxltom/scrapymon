from wsgi import app
import unittest


class TestIndexBlueprint(unittest.TestCase):
    """Test the index blueprint."""
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index_blueprint(self):
        rv = self.app.get('/_test')
        self.assertEqual(rv.status_code, 404)
