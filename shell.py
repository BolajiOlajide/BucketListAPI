"""
Create an context for access the application from an interactive shell.

Write a function to import all the context and objects needed for a shell
prompt.
"""
import os

from app.models import User, BucketList, Items
from app import db, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def make_shell_context():
    """
    Create a context for interacting in a shell for the application.

    Import the model objects to enable easy interaction.
    """
    return dict(app=app, db=db, User=User, BucketList=BucketList, Items=Items)
