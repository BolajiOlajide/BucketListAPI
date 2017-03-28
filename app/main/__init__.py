"""
Create the Blueprint.

Create and import the views to be used for the Blueprint
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes
