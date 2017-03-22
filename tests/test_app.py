"""
Basic Test Case.

Test the basic settings of the application to be certain it's functioning well.
"""
import unittest

from flask import current_app

from app import db, create_app


class BasicTestCase(unittest.TestCase):
    """
    The class encompasses all the test cases related to the Basic Application.

    I wrote simple tests to check for correct application instances and other
    if the application exists etc.
    """

    def setUp(self):
        """
        Set up the application for testing.

        The method 'setUp' simply starts the application in test mode and
        initializes all necessary requirements.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """
        Check if the application has started.

        The test method checks that there is a current instance of the
        Flask application running currently.
        """
        self.assertFalse(current_app is None)

    def test_app_config_is_testing(self):
        """
        Check the configuration which the application is running on.

        In the setup method, we chose the testing configuration to start the
        application so we test that that is the correct configuration.
        """
        self.assertTrue(current_app.config['TESTING'])
