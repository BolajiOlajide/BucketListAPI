"""
Authentication settings for the BucketList API.

Password verification and user registration takes place here.
"""
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from . import authentication
from app import errors
from app.decorators import json
from app.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, password):
    """
    Verify token.

    Verify token, password doesn't need to be present here. The token is
    going to be in the request headers always.
    """
    user = User.verify_auth_token(token)

    if not user:
        return False

    g.user = user
    return True


@authentication.route('/login', methods=['POST'])
def login():
    """
    Verify user name & password.

    Verify the user's identity using the username and password and returns
    a token.
    """
    if not request.json:
        return errors.bad_request("No JSON file detected.")

    username = request.json.get('username')
    password = request.json.get('password')

    if not (username and password):
        return errors.bad_request("username or password missing.")

    user = User.query.filter_by(username=username).first()
    if not (user and user.verify_password(password)):
        return errors.unauthorized("Username and password doesn't match.")

    token = user.generate_auth_token()
    return jsonify({'token': token}), 200


@authentication.route('/register', methods=['POST'])
@json
def register_user():
    """
    Create a new user.

    Using the supplied information in the body of the request, a new user is
    created using the user name & password provided.
    """
    if not request.json:
        return errors.bad_request("No JSON file detected.")

    username = request.json.get('username')
    password = request.json.get('password')

    if not (username and password):
        return errors.bad_request("username or password missing.")

    if User.query.filter_by(username=username).first():
        return errors.bad_request("username already exist.")

    try:
        user = User(username=username)
        user.hash_password(password)
        user.save()
        return user, 201
    except:
        return errors.bad_request("An error occurred while saving. "
                                  "Please try again.")


@auth.error_handler
def auth_error():
    """
    Handle authentication errors.

    Handle all auth errors.
    """
    return errors.token_error('Invalid credentials')
