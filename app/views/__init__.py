"""
Create the Blueprint for the views.

Create and import the views to be used for the Blueprint
"""
from flask import Blueprint

view = Blueprint('view', __name__)

from . import forms, views
