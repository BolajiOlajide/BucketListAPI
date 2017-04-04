"""
Routes Test Case.

Test the routes of the application to be certain it's functioning well.
"""

import json
import unittest

from flask import g, url_for

from app import db, create_app
from app.models import User, BucketList, Items
from tests.header import create_api_headers


class TestAPIRoutes(unittest.TestCase):
    """
    Test all the routes in the API.BucketList.

    Test all routes and also set up variables to be used while testing below.
    """

    default_username = 'andela'
    default_password = 'andela'
    another_user = 'proton'
    bucketlist_name = "Proton's BucketList"
    bucketlist_item_name = 'Meet Njira'
    bucketlist2_name = "Ichiato's BucketList"
    bucketlist_item2_name = 'Slap Koya'
    bucketlist3_name = "Njira's BucketList"
    bucketlist_item3_name = 'Visit Olumo Rock'

    def setUp(self):
        """
        Set up the application for testing.

        The method 'setUp' simply starts the application in test mode and
        initializes all necessary requirements.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        user = User(username=self.default_username)
        user.hash_password(self.default_password)
        user2 = User(username=self.another_user)
        user2.hash_password(self.default_password)
        db.session.add_all([user, user2])
        db.session.commit()
        g.user = user
        bucketlist = BucketList(name=self.bucketlist_name,
                                created_by=user.user_id)
        bucketlist2 = BucketList(name=self.bucketlist2_name,
                                 created_by=user2.user_id)
        bucketlist3 = BucketList(name=self.bucketlist3_name,
                                 created_by=user.user_id)
        db.session.add_all([bucketlist, bucketlist2, bucketlist3])
        db.session.commit()
        self.token = user.generate_auth_token()

        bucketlist_item = Items(
            name=self.bucketlist_item_name,
            done="false",
            bucketlist_id=bucketlist.bucketlist_id
        )
        bucketlist_item2 = Items(
            name=self.bucketlist_item2_name,
            done="false",
            bucketlist_id=bucketlist2.bucketlist_id
        )
        bucketlist_item3 = Items(
            name=self.bucketlist_item3_name,
            done="false",
            bucketlist_id=bucketlist3.bucketlist_id
        )
        db.session.add_all([bucketlist_item, bucketlist_item2,
                            bucketlist_item3])
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Tear down method.

        This method removes every information related to the test cases.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_bucketlists(self):
        """
        Test the get_bucketlists endpoint.

        Test the route that gets all the BucketLists and also check the status
        code it returns.
        """
        print self.token
        response = self.client.get(
            url_for('main.get_bucketlists'),
            headers=create_api_headers(self.token))
        self.assertEquals(response.status_code, 200)

    def test_get_bucketlists_with_limit(self):
        """
        Test the get_bucketlists endpoint.

        Test the route that gets all the BucketLists with the limit query and
        also check the status code it returns.
        """
        response = self.client.get(
            url_for('main.get_bucketlists'), query_string={'limit': '1'},
            headers=create_api_headers(self.token))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['meta']['limit'], 1)

    def test_get_bucketlists_with_max_limit(self):
        """
        Test the get bucketlists endpoint.

        Test the route that gets all the BucketList with a limit query.
        """
        response = self.client.get(
            url_for('main.get_bucketlists'), query_string={'limit': '120'},
            headers=create_api_headers(self.token))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['meta']['limit'], 100)

    def test_get_bucketlists_with_search(self):
        """
        Test the get bucketlists endpoint.

        Test the route that gets all the BucketList with a search query.
        """
        response = self.client.get(
            url_for('main.get_bucketlists'), query_string={'q': 'Proton'},
            headers=create_api_headers(self.token))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['bucketlists'][0]['name'],
                          "Proton's BucketList")

    def test_get_bucketlist(self):
        """
        Test the main.get_bucketlist endpoint.

        Get a bucketlist by id and test if the status code returned is 200
        """
        response = self.client.get(
            url_for('main.get_bucketlist', list_id=1),
            headers=create_api_headers(self.token))
        self.assertEquals(response.status_code, 200)

    def test_get_nonexistent_bucketlist(self):
        """
        Test the get bucketlist endpoint.

        Test that this endpoint returns a 404 status code when the resource
        cannot be found.
        """
        response = self.client.get(
            url_for('main.get_bucketlist', list_id=120),
            headers=create_api_headers(self.token))
        self.assertEquals(response.status_code, 404)

    def notest_create_bucketlist(self):
        """
        Test the create_bucketlist endpoint.

        Test the status code and json object returned when a new bucketlist is
        created.
        """
        response = self.client.post(
            url_for('main.create_bucketlist'),
            data=json.dumps({"name": "Proton's BucketList"}),
            headers=create_api_headers(self.token))
        data = json.loads(response.get_data(as_text=True))
        print data
        # self.assertEquals(data['name'], "Proton's BucketList")
        self.assertEquals(response.status_code, 201)

    def test_create_bucketlist_with_keyerror(self):
        """
        Test the create_bucketlist endpoint.

        Test the status code and json object returned when a new bucketlist is
        created.
        """
        response = self.client.post(
            url_for('main.create_bucketlist'),
            data=json.dumps({"names": "Proton's BucketList"}),
            headers=create_api_headers(self.token))
        self.assertEquals(response.status_code, 400)
