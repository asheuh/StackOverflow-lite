from unittest import TestCase
from stackoverflow import create_app, settings

class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(settings.TESTING)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """removes the db and the context"""
        self.app_context.pop()
