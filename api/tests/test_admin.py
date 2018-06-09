"""
This module include tests to the admin endpoints of the API ie
    - approve request
    - disapprove request
    - resolve request

"""

import unittest
import json
from api import create_app
from migration import migration
from flask import json


class TestAdmin(unittest.TestCase):
    """
        Class to hold our tests
    """

    def setUp(self):
        """ this is run before each test """
        self.app = create_app(config_name="testing")
        self.app_client = self.app.test_client()

        self.sample_user = {
            "first_name": "Bob",
            "last_name": "Burgers",
            "email": "bob@example.com",
            "password": "pass1#Ps",
            "confirm_password": "pass1#Ps"
        }
        self.sample_admin = {
            "first_name": "Alice",
            "last_name": "Burgers",
            "email": "alice@example.com",
            "password": "pass1#Ps",
            "confirm_password": "pass1#Ps"
        }
        self.sample_request = {
            "title": "Fix mouses",
            "description": "mouses in lab 2 not working",
            "status": "open",
            "type": "Repair",
        }
        self.sample_request2 = {
            "title": "Replace monitors",
            "description": "monitors in lab 2 not working",
            "status": "open",
            "type": "Maintenance",
        }
        # run migrations before each test
        migration()
    
    def get_token_admin(self):
        """ create and login admin to get token """
        # login super admin
        response = self.app_client.post('/api/v1/auth/login',
                                        data=json.dumps({'email': 'admin@admin.tec',
                                               'password': 'admin'}),
                                        content_type="application/json")
        result = json.loads(response.data)
        headers = {'access-token': result['access-token']}

        response = self.app_client.post('/api/v1/admin', 
                                        data=json.dumps(self.sample_admin),
                                        content_type="application/json",
                                        headers=headers)
        
        response = self.app_client.post('/api/v1/auth/login',
                                        data=json.dumps(self.sample_admin),
                                        content_type="application/json")
        result = json.loads(response.data)        
        return {'access-token': result['access-token']}

    def insert_requests(self):
        """ helper method to insert request to db """
        response = self.app_client.post('/api/v1/auth/register',
                                          data=json.dumps(self.sample_user),
                                          content_type="application/json")

        response = self.app_client.post('/api/v1/auth/login',
                                          data=json.dumps(self.sample_user),
                                          content_type="application/json")
        result = json.loads(response.data)
        headers = {'access-token': result['access-token']}

        response = self.app_client.post('/api/v1/users/requests',
                                          data=json.dumps(self.sample_request),
                                          content_type="application/json",
                                          headers=headers)
        response = self.app_client.post('/api/v1/users/requests',
                                          data=json.dumps(self.sample_request2),
                                          content_type="application/json",
                                          headers=headers)

    def test_create_admin(self):
        """ test whether super admin can create admin """
        # login super admin
        response = self.app_client.post('/api/v1/auth/login',
                                        data=json.dumps({'email': 'admin@admin.tec',
                                               'password': 'admin'}),
                                        content_type="application/json")
        result = json.loads(response.data)
        access_token = result['access-token']
        self.assertEqual(response.status_code, 200)
        headers = {'access-token': access_token}

        response = self.app_client.post('/api/v1/admin', 
                                        data=json.dumps(self.sample_admin),
                                        content_type="application/json",
                                        headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_admin_get_requests(self):
        """ test that an admin can retrieve all requests or by id
            and if none exists return a relevant message 
        """
        headers = self.get_token_admin() 

        # try fetch while no requests exist
        response1 = self.app_client.get('/api/v1/requests', headers=headers)
        self.assertEqual(response1.status_code, 404)

        #try fetch by id no requests
        response1 = self.app_client.get('/api/v1/requests/1', headers=headers)
        self.assertEqual(response1.status_code, 404)
        self.insert_requests()

        #test admin get by ID
        response = self.app_client.get('/api/v1/requests/1', headers=headers)
        self.assertEqual(response.status_code, 200)

        #test admin get all
        response = self.app_client.get('/api/v1/requests', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_approve_request(self):
        """ test that an admin can approve a request
            and if none exists return a relevant message 
        """
        headers = self.get_token_admin() 

        # try approve while request does not exist
        response1 = self.app_client.put('/api/v1/requests/1/approve', headers=headers)
        self.assertEqual(response1.status_code, 404)

        self.insert_requests()

        #test approve while ID exists
        response = self.app_client.put('/api/v1/requests/1/approve', headers=headers)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_admin_disapprove_request(self):
        """ test that an admin can disapprove a request
            and if none exists return a relevant message 
        """
        headers = self.get_token_admin() 

        # try disapprove while request does not exist
        response1 = self.app_client.put('/api/v1/requests/1/disapprove', headers=headers)
        self.assertEqual(response1.status_code, 404)

        self.insert_requests()

        #test disapprove while ID exists
        response = self.app_client.put('/api/v1/requests/1/disapprove', headers=headers)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_admin_resolve_request(self):
        """ test that an admin can resolve a request
            and if none exists return a relevant message 
        """
        headers = self.get_token_admin() 

        # try resolve while request does not exist
        response1 = self.app_client.put('/api/v1/requests/1/resolve', headers=headers)
        self.assertEqual(response1.status_code, 404)

        self.insert_requests()

        #test resolve while ID exists
        response = self.app_client.put('/api/v1/requests/1/resolve', headers=headers)
        print(response)
        self.assertEqual(response.status_code, 200)
        
    def tearDown(self):
        migration()