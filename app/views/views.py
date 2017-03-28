"""
Define the view routes.

Define the routes for the front-end to interact with the API
"""
from flask import render_template

from . import view


@view.route('/')
def index():
    """
    Index route.

    This route is for the home page.
    """
    # return "<h1> App WORKS! </h1>"
    return render_template('index.html')
