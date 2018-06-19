from unittest import TestCase

from scrapymon.app import create_app, db


class FlaskTestCase(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Update to in-memory db for test
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Suggested to be after modifying app configurations
        self.app_context = self.app.test_request_context()
        self.app_context.push()

        # Initialize db
        db.create_all(bind=None)

    def tearDown(self):
        db.session.remove()

        # Drop db
        db.drop_all(bind=None)

        # Must after all operations
        self.app_context.pop()
