import unittest
from config import Config
from scrapymon import create_app
from scrapymon.views.index.views import _list_projects, _list_spiders


class TestIndex(unittest.TestCase):
    """Test index blueprint."""

    def setUp(self):
        """Initialize tests."""
        app = create_app(Config(
            bootstrap=True,
            db=True,
            httpauth=True,
            index=True,
        ))
        app.app_context().push()

    def test_list_projects_spiders(self):
        """Test _list_projects and _list_spiders function"""
        projects = _list_projects()
        self.assertEqual(type(projects), list)
        self.assertTrue(len(projects) > 0)

        spiders = _list_spiders(projects[0])
        self.assertEqual(type(spiders), list)
        self.assertTrue(len(spiders) > 0)

