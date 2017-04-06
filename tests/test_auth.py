"""
Test Authentication.

Test user authentication and token generation.
"""
import unittest
import json

from flask import url_for

from app import db, create_app
from app.models import User


class TestUserModel(unittest.TestCase):
    """
    The class encompasses all test cases related to the Application's model.

    I wrote simple tests to test the models.
    """

    def setUp(self):
        """
        Set up the application for testing.

        The method 'setUp' simply starts the application in test mode.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(username='njirap')
        self.user.hash_password('andela')
        self.user.save()

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_encode_decode_auth_token(self):
        """
        Test the encoded token.

        This test whether the token returned is in bytes.
        """
        auth_token = self.user.generate_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(
            User.verify_auth_token(auth_token).user_id == self.user.user_id)

    def test_register(self):
        """
        Test register user.

        This tests user registration route.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.register_user'),
                data=json.dumps({'username': 'proton', 'password': 'andela'}),
                content_type='application/json'
            )
        data = json.loads(response.data.decode())
        self.assertTrue(data['username'] == "proton")
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_protected_routes(self):
        """
        Test protected routes.

        Check that protected routes can't be accessed without tokens.
        """
        response = self.client.get(url_for('main.get_bucketlists'),
                                   content_type='application/json')
        self.assertEquals(response.status_code, 401)

    def test_login(self):
        """
        Test the login route.

        This test checks if a user is successful logged in and the status
        code returned.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data=json.dumps({'username': 'njirap', 'password': 'andela'}),
                content_type='application/json'
            )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_without_json(self):
        """
        Test login without json.

        Test that when a user tries to logging without sending a JSON object,
        the API flags it as an error.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data={'username': 'njirap', 'password': 'andela'},
            )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_with_null_password(self):
        """
        Test if a user can supply a null password.

        This test checks if the user supplies a null string as username or
        password.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data=json.dumps({'username': 'njirap', 'password': ''}),
                content_type='application/json'
            )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_credentials(self):
        """
        Test user signing in with wrong credentials.

        When a user logs in with wrong credentials, the API should return a
        400 error.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data=json.dumps({'username': 'njirap', 'password': 'percila'}),
                content_type='application/json'
            )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
