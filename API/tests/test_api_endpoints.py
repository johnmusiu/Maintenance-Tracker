"""
This module include tests to the different endpoints of the API

"""

import unittest
import json
from API import APP


class TestAPIAuth(unittest.TestCase):
    """
        Class to hold our tests
    """

    def setUp(self):
        """ this is run before each test """
        APP.testing = True
        self.app = APP.test_client()
        self.sample_user = {
            "name": "Bob Burgers",
            "email": "bob@example.com",
            "password": "pass",
        }


    def test_user_signup(self):
        """
            Test API user signup with all details provided correct
        """
        response = self.app.post('/auth/register/', 
                                data=json.dumps(self.sample_user), 
                                content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["email"], "bob@example.com")
        self.assertEqual(result["name"], "Bob Burgers")
        self.assertEqual(response.status_code, 201)
    
    def test_signup_null_field(self):
        """ test user signup given email/name/password provided is null """
        self.sample_user['email'] = ""
        response = self.app.post('/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please fill in required email field then try again!")
        self.assertEqual(response.status_code, 400)         

    def test_signup_invalid_email(self):
        """ Test if user signup is done using an invalid email address"""
        self.sample_user['email'] = "bob@232"
        response = self.app.post('/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please provide a valid email address!")
        self.assertEqual(response.status_code, 400)        

if __name__ == "__main__":
    unittest.main()


    

