import os

from .flask_test_case import FlaskTestCase

import scrapymon as project


class AppTestCase(FlaskTestCase):

    def setUp(self):
        super().setUp()

        # Make sure using dev settings in testing
        self.assertEqual(
            os.environ.get('{}_CONFIG'.format(project.__name__.upper())), 'dev'
        )
        self.assertEqual(self.app.config['TESTING'], True)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'].endswith(':memory:')
        )

        # Test project dependent environment variables
        pass
