"""
Models Test Case.

Test the models of the application to be certain it's functioning well.
"""

import unittest

from app import db, create_app
from app.models import User, BucketList, Items


class UserModelTestCase(unittest.TestCase):
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

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        """
        Test password.

        Test the password is actually hashed and exists.
        """
        u = User(username='test')
        u.hash_password('cat')
        self.assertTrue(u.hash_password is not None)

    def test_password_hash_isnt_similar(self):
        """
        Test password hash.

        Test identical passwords return disimilar password hashes.
        """
        u = User(username='test')
        u.hash_password('cat')
        u2 = User(username='test2')
        u2.hash_password('cat')
        self.assertTrue(u.hash_password != u2.hash_password)

    def test_password_hash(self):
        """
        Test the hashed password.

        Check if the hashed password is the same as the password when it has
        been decrypted.
        """
        u = User(username="bolaji")
        password = 'andela'
        u.hash_password(password)
        self.assertTrue(u.verify_password(password))


if __name__ == '__main__':
    unittest.main()
