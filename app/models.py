"""
Define SQLAlchemy models.

The SQLAlchemy models for the database is defined here.
"""

import datetime

from flask import current_app, url_for
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class Base(db.Model):
    """
    Base class for models.

    Define the base class for the models so others can inherit from it.
    """

    __abstract__ = True

    date_created = db.Column(
        db.DateTime, default=datetime.datetime.now(), nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.datetime.now(),
        onupdate=datetime.datetime.now(), nullable=False)

    def save(self):
        """
        Save to database.

        Save instance of the object to database and commit.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete from database.

        Deletes instance of an object from database
        """
        db.session.delete(self)
        db.session.commit()


class User(Base):
    """
    Set up the User model.

    Set up the properties of the User object and the table name too.
    """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True,
                         nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def hash_password(self, password):
        """
        Hash user password.

        Passwords shouldn't be stored as string so we hash them.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verify password.

        Use the pwd_context to decrypt the password hash and confirm if it
        matches the initial password set by the user.
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=36000):
        """
        Generate token.

        This function generates a token to be used by the user for requests.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        """
        Verify token.

        Verify that the token is valid and return the user id.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None

            # valid token, but expired
        except BadSignature:
            return None

            # invalid token
        user = User.query.get(data['id'])
        return user

    def to_json(self):
        """
        Display the object properties as a json object.

        Mold up all the properties of User object into an object for display.
        """
        return {
            'username': self.username
        }

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the User object.
        """
        return '<User: {}>'.format(self.username)


class BucketList(Base):
    """
    Set up the BucketList model.

    Define the properties of the BucketList object and the table name too.
    """

    __tablename__ = 'bucketlist'
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                           nullable=False)

    def to_json(self):
        """
        Display the object properties as a json object.

        Mold up all the properties of BucketList object into
        an object for display.
        """
        items = [item.to_json() for item in self.items]
        return {
            'id': self.bucketlist_id,
            'name': self.name,
            'items': items,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'bucketlist_url': self.get_url(),
            'created_by': self.created_by
        }

    def from_json(self, json):
        """
        Read from an object.

        Read from a json object, properties of a BucketList object.
        """
        try:
            self.name = json['name']
        except KeyError as e:
            raise ValueError('Invalid name: missing ' + e.args[0])
        return self

    def get_url(self):
        """
        Get the URL for this instance.

        Returns the URL of the instance of the BucketList.
        """
        return url_for('main.get_bucketlist', list_id=self.bucketlist_id,
                       _external=True)

    @staticmethod
    def get_bucketlists_url():
        """
        Get the URL of bucketlists.

        Returns the URL of all the bucketlists at once.
        """
        return url_for('main.get_bucketlists', _external=True)

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the BucketList object.
        """
        return '<BucketList: {}>'.format(self.name)


class Items(Base):
    """
    Set up the Items model.

    Define the properties of the Items object and the table name too.
    """

    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey('bucketlist.bucketlist_id'), nullable=False
    )
    bucketlist = db.relationship(
        'BucketList',
        backref=db.backref(
            'items',
            cascade="all,delete-orphan"
        ),
        lazy='joined'
    )

    def to_json(self):
        """
        Display the object properties as a json object.

        Mold up all the properties of Items object into
        an object for display.
        """
        return {
            'id': self.item_id,
            'name': self.name,
            'done': self.done,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    def from_json(self, json):
        """
        Read from an object.

        Read from a json object, properties of a Items object.
        """
        if 'done' in json:
            done = json['done'].lower()
            self.done = bool(1 if done == 'true' else 0)
        if 'name' in json:
            self.name = json['name']
        if not self.name:
            raise ValueError(
                'Invalid argument {}. `name` and `done` are the only '
                'keys allowed'.format(json.keys()))
        return self

    def get_url(self):
        """
        Get the URL for this instance.

        Returns the URL of the instance of the BucketList.
        """
        return url_for('api.get_bucketlist_item',
                       bucketlist_id=self.bucketlist_id,
                       item_id=self.item_id,
                       _external=True)

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the Items object.
        """
        return '<Item: {}>'.format(self.name)
