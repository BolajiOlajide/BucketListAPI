"""
Authentication settings for the BucketList API.

Password verification and user registration takes place here.
"""
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from . import authe
from app import errors
from app.decorators import json
from app.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
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


@authe.route('/login', methods=['POST'])
def login():
    """
    Verify a user's identity.

    Verify the user's identity and returns a token.
    """
    if not request.json:
        return errors.bad_request("No JSON file detected.")

    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return errors.bad_request("username or password missing.")

    user = User.query.filter_by(username=username).first()
    if not user:
        return errors.bad_request("Username and password doesn't match.")

    if not user.verify_password(password):
        return errors.bad_request("Username and password doesn't match.")

    g.user = user
    token = user.generate_auth_token()
    return jsonify({'token': token})


@authe.route('/register', methods=['POST'])
@json
def register_user():
    """
    Create a new user.

    Creates a new user in the application.
    """
    if not request.json:
        return errors.bad_request("No JSON file detected.")

    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
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


@authe.route('/token')
def get_auth_token():
    """
    Generate a token.

    When a user is verified, a token is sent to process the requests.
    """
    try:
        token = g.user.generate_auth_token()
    except:
        return jsonify({'Error': 'No User is logged in.'}), 401
    return jsonify({'token': token.decode('ascii')})
