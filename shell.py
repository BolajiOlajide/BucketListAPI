"""
Create an context for access the application from an interactive shell.

Write a function to import all the context and objects needed for a shell
prompt.
"""
from os import environ
from os.path import join, dirname

from dotenv import load_dotenv

from app.models import User, BucketList, Items
from app import db, create_app

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = create_app(environ.get('FLASK_CONFIG'))


def make_shell_context():
    """
    Create a context for interacting in a shell for the application.

    Import the model objects to enable easy interaction.
    """
    return dict(app=app, db=db, User=User, BucketList=BucketList, Items=Items)
