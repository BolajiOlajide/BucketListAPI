"""
Define forms.

The forms to be used in this view are defined here.
"""

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    """
    The LoginForm class.

    This handles the form fields for login to the API.
    """

    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Keep me signed in.')
    submit = SubmitField()


class RegisterForm(Form):
    """
    The RegisterForm class.

    Handles the form fields for user registration.
    """

    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField()
