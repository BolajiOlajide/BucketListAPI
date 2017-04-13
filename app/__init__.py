"""
Setup an initialization to delay the creation of the application after runtime.

This helps to enable the use of blueprint.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    """
    Initialize the application after runtime.

    This is done to enable the use of Blueprint.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    # Register the authentication blueprint in the application instance.
    from auth import authentication as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Link to the blueprint script for the routes
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')

    return app
