import unittest

from scrapymon.config import Config
from scrapymon.app import create_app
from scrapymon.blueprints.index import (_list_projects, _list_versions,
                                        _list_spiders, _list_jobs)


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

    def test_list_projects_versions_spiders_jobs(self):
        """Test _list_projects, _list_versions,  _list_spiders, _list_jobs."""
        projects = _list_projects()
        self.assertEqual(type(projects), list)
        self.assertTrue(len(projects) > 0)

        versions = _list_versions(projects[0])
        self.assertEqual(type(versions), list)
        self.assertTrue(len(versions) > 0)

        spiders = _list_spiders(projects[0])
        self.assertEqual(type(spiders), list)
        self.assertTrue(len(spiders) > 0)

        pending_jobs, running_jobs, finished_jobs = _list_jobs(projects[0])
        self.assertEqual(type(pending_jobs), list)
        self.assertEqual(type(running_jobs), list)
        self.assertEqual(type(finished_jobs), list)
