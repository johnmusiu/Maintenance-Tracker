"""
This module include tests to the different endpoints of the API

"""

import unittest
import json
from API import app


class TestAPIAuth(unittest.TestCase):
    """
        Class to hold our tests
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


    def test_user_signin(self):
        """
            Test API user signin with correct credentials
        """
        response = self.app_client.post('/auth/register', 
                                data=json.dumps(self.sample_user), 
                                content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.app_client.post('/auth/login',
                                data=json.dumps(self.sample_user),
                                content_type="application/json")
        
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"], "Login success, welcome!")

    def test_signin_null_field(self):
        """ test user signin given email/password provided is null """
        #test with empty email
        self.sample_user['email'] = ""
        response = self.app_client.post('/auth/login', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'email' field")
        self.assertEqual(response.status_code, 400) 

        #test with empty password
        self.sample_user['email'] = "bob@example.com"
        self.sample_user['password'] = ""
        response1 = self.app_client.post('/auth/login', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result1 = json.loads(response1.data)
        self.assertEqual(result1["message"], "Please fill in the 'password' field")
        self.assertEqual(response1.status_code, 400)        

    def test_signin_invalid_email(self):
        """ Test user signin using an invalid email address"""
        self.sample_user['email'] = "bob@232"
        response = self.app_client.post('/auth/login', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please enter a valid email address!")
        self.assertEqual(response.status_code, 400)  

if __name__ == "__main__":
    unittest.main()