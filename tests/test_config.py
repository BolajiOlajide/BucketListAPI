"""
Configuration Test Case.

Test the configuration of the application to be certain it's functioning well.
"""
from os import environ
from os.path import join, abspath, dirname
import unittest

from dotenv import load_dotenv
from flask import current_app

from app import create_app

basedir = abspath(dirname(dirname(__file__)))
dotenv_path = join(basedir, '.env')
load_dotenv(dotenv_path)


class TestDevelopmentConfig(unittest.TestCase):
    """
    Test the configuration for Development mode.

    This test asserts that the different configurations have been set properly.
    """

    def setUp(self):
        """
        Start the application in development mode.

        Using the config defined in the config.py this uses that to test the
        application.
        """
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        self.app_context.pop()

    def test_app_is_development(self):
        """
        Test the development configuration.

        Test that DEBUG and SQLALCHEMY_TRACK_MODIFICATIONS are set to True and
        the database used is the local one.
        """
        self.assertTrue(self.app.config['DEBUG'])
        self.assertFalse(current_app is None)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            environ.get("DATABASE_URI")
        )
        self.assertTrue(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])


class TestTestingConfig(unittest.TestCase):
    """
    Test the configuration for Testing mode.

    This test asserts that the different configurations have been set properly.
    """

    def setUp(self):
        """
        Start the application in testing mode.

        Using the config defined in the config.py this uses that to test the
        application.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        self.app_context.pop()

    def test_app_is_testing(self):
        """
        Test the testing configuration.

        Test that DEBUG and SQLALCHEMY_TRACK_MODIFICATIONS are set to True and
        the database used is the local one.
        """
        dbase = environ.get("TEST_DB")
        self.assertFalse(self.app.config['USE_RATE_LIMITS'])
        self.assertTrue(self.app.config['SQLALCHEMY_DATABASE_URI'] == dbase)


class TestProductionConfig(unittest.TestCase):
    """
    Test the configuration for Production mode.

    This test asserts that the different configurations have been set properly.
    """

    def setUp(self):
        """
        Start the application in Production mode.

        Using the config defined in the config.py this uses that to test the
        application.
        """
        self.app = create_app('production')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        self.app_context.pop()

    def test_app_is_prod_mode(self):
        """
        Test the testing configuration.

        Test that DEBUG and SQLALCHEMY_TRACK_MODIFICATIONS are set to True and
        the database used is the local one.
        """
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            environ.get("DATABASE_URI")
        )
