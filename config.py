"""
Configuration settings for the Bucket List API.

The definition of the different configuration settings is contained here:
- Development Configuration
- Testing Configuration
- Production Configuration
"""

import os


class Config:
    """
    The definition of the global configuration is defined here.

    Attributes such as SECRET_KEY are the same no matter the platform used.
    """

    SECRET_KEY = 'u35dfh___vv@$%%jkdsvjkhb___jdfnv93043klm__vdmkll55vd----__'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_TOKEN_AUTH = True
    DEBUG = False
    SSLIFY_SUBDOMAINS = True
    DEFAULT_PER_PAGE = 2
    MAX_PER_PAGE = 3

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

    SQLALCHEMY_DATABASE_URI = 'postgresql://bolaji:andela@localhost/bucketlist'
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
    SQLALCHEMY_DATABASE_URI = 'postgres://rkswjhal:Z_eG-nhn-_DqTEHpxCxjm6OV568FnG6Y@stampy.db.elephantsql.com:5432/rkswjhal'


class ProductionConfig(Config):
    """
    The configuration settings for production mode is defined here.

    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called ProductionConfig.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


# Object containing the different configuration classes.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
