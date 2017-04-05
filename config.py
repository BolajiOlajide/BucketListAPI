"""
Configuration settings for the Bucket List API.

The definition of the different configuration settings is contained here:
- Development Configuration
- Testing Configuration
- Production Configuration
"""
import os
from os.path import join, dirname

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    """
    The definition of the global configuration is defined here.

    Attributes such as SECRET_KEY are the same no matter the platform used.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_TOKEN_AUTH = True
    DEBUG = False
    SSLIFY_SUBDOMAINS = True
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100

    @staticmethod
    def init_app(app):
        """
        Initialize the application.

        This static method initializes the application using whatever
        configuration the user has chosen.
        """
        pass


class DevelopmentConfig(Config):
    """
    The configuration settings for development mode is defined here.

    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called DevelopmentConfig.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class TestingConfig(Config):
    """
    The configuration settings for testing mode is defined here.

    Attributes such as SQLALCHEMY_DATABASE_URI, TESTING are different for other
    modes, so they are defined in a class called TestingConfig.
    """

    USE_RATE_LIMITS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DB")
    SERVER_NAME = os.environ.get("SERVER_NAME")


class ProductionConfig(Config):
    """
    The configuration settings for production mode is defined here.

    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called ProductionConfig.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


# Object containing the different configuration classes.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
