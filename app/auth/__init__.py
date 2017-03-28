"""
Create the Blueprint.

Create and import the views to be used for the Blueprint
"""
from flask import Blueprint

authe = Blueprint('authe', __name__)

from . import routes