"""
This module include tests to the different endpoints of the API

"""

import unittest
import json
from API import app

class TestAPIRequests(unittest.TestCase):
    """
        Class to hold our tests about:
            - user adding a maintenance request
            - user updating a maintenance request
            - user viewing all their maintenance requests
            - user viewing a single maintenance request
    """

    def setUp(self):
        """ this is run before each test """
        app.testing = True
        self.app_client = app.test_client()
        self.sample_user = {
            "name": "Bob Burgers",
            "email": "bob@example.com",
            "password": "pass",
        }

        self.sample_request = {
            "title": "Fix mouses",
            "description": "mouses in lab 2 not working",
            "status": "ongoing",
            "type": "maintenance",
            "created_at": "",
            "completed_at": "",
            "user_id": 1
        }

    # begin tests for api create request
    def test_api_can_create_request(self):
        """
            Test API make maintenance request with all details provided correctly
        """
        response = self.app_client.post('/users/requests/', 
                                data=json.dumps(self.sample_request), 
                                content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Maintenance request submitted successfully.")
        self.assertEqual(result["title"], "Fix mouses")
        self.assertEqual(response.status_code, 201)
    
    def test_create_request_with_null_field(self):
        """ 
            test whether null input raises error for fields
            title/description/type
        """
        # test for null title
        self.sample_request['title'] = ""
        response = self.app_client.post('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'title' field")
        self.assertEqual(response.status_code, 400)

        # test for null description
        self.sample_request['title'] = "Fix mouses"
        self.sample_request['description'] = ""
        response = self.app_client.post('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'description' field")
        self.assertEqual(response.status_code, 400)

        # test for null request type
        self.sample_request['description'] = "mouses in lab 2 not working"
        self.sample_request['type'] = ""
        response = self.app_client.post('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'type' field")
        self.assertEqual(response.status_code, 400)

    def test_create_request_with_invalid_type(self):
        """ 
            test that using a type other than maintenance or repair 
            returns a value error
        """
        self.sample_request['type'] = "Another type"
        response = self.app_client.post('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Type can only be Maintenance or Repair")
        self.assertEqual(response.status_code, 400)
    # end tests for api create task

    # begin tests for api update request
    def test_api_can_update_request(self):
        """ test user can update a request that is not resolved """
        response = self.app_client.post('/users/requests/', 
                                data=json.dumps(self.sample_request), 
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # update values on data to be submitted
        self.sample_request['title'] = "Fix mouses and keyboards"
        self.sample_request['description'] = "Mouses and keyboards in lab 2 not working"
        response1 = self.app_client.put('/users/requests/1', 
                                    data=json.dumps(self.sample_request),
                                    content_type='application/json')

        result1 = json.loads(response1.data)
        self.assertEqual(result1["title"], "Fix mouses and keyboards")
        self.assertEqual(result1["message"], "Maintenance request updated successfully.")
        self.assertEqual(response.status_code, 200)
    
    def test_update_request_with_null_field(self):
        """ 
            test whether null input raises error for fields
            title/description/type
        """
        #insert request
        response = self.app_client.post('/users/requests/', 
                                data=json.dumps(self.sample_request), 
                                content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

        # test for null title
        self.sample_request['title'] = ""
        response = self.app_client.put('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'title' field")
        self.assertEqual(response.status_code, 400)

        # test for null description
        self.sample_request['title'] = "Fix mouses"
        self.sample_request['description'] = ""
        response = self.app_client.put('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'description' field")
        self.assertEqual(response.status_code, 400)

        # test for null request type
        self.sample_request['description'] = "mouses in lab 2 not working"
        self.sample_request['type'] = ""
        response = self.app_client.put('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'type' field")
        self.assertEqual(response.status_code, 400)

    def test_update_request_with_invalid_type(self):
        """ 
            test that using a type other than maintenance or repair 
            returns a value error
        """
        self.sample_request['type'] = "Another type"
        response = self.app_client.post('/users/requests/', 
                                    data=json.dumps(self.sample_request),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Type can only be Maintenance or Repair")
        self.assertEqual(response.status_code, 400)
    # end tests for update request
    
    def tearDown(self):
        """ teardown all initialized variables """
        return True

if __name__ == "__main__":
    unittest.main()