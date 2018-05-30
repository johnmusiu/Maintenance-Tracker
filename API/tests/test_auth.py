"""
This module include tests to the auth endpoints of the API ie
    - api user signup (/auth/register)
    - api user signin (/auth/login)

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

    # begin tests for api user signin
    def test_user_signin(self):
        """
            Test API user signin with correct credentials
        """
        response = self.app_client.post('/api/v1/auth/register', 
                                data=json.dumps(self.sample_user), 
                                content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.app_client.post('/api/v1/auth/login',
                                data=json.dumps(self.sample_user),
                                content_type="application/json")
        
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"], "Login success, welcome!")

    def test_signin_null_field(self):
        """ test user signin given email/password provided is null """
        #test with empty email
        self.sample_user['email'] = ""
        response = self.app_client.post('/api/v1/auth/login', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Please fill in the 'email' field")
        self.assertEqual(response.status_code, 400) 

        #test with empty password
        self.sample_user['email'] = "bob@example.com"
        self.sample_user['password'] = ""
        response1 = self.app_client.post('/api/v1/auth/login', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result1 = json.loads(response1.data)
        self.assertEqual(result1["message"], "Please fill in the 'password' field")
        self.assertEqual(response1.status_code, 400)        

    def test_signin_invalid_email(self):
        """ Test user signin using an invalid email address"""
        self.sample_user['email'] = "bob@232"
        response = self.app_client.post('/api/v1/auth/login', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please enter a valid email address!")
        self.assertEqual(response.status_code, 400)  
    # end tests for api user signin

    # begin tests for api user signup 
    def test_user_signup(self):
        """
            Test API user signup with all details provided correct
        """
        response = self.app_client.post('/api/v1/auth/register/', 
                                data=json.dumps(self.sample_user), 
                                content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["email"], "bob@example.com")
        self.assertEqual(result["name"], "Bob Burgers")
        self.assertEqual(response.status_code, 201)
    
    def test_signup_null_field(self):
        """ test user signup given email/name/password provided is null """
        #test with empty email
        self.sample_user['email'] = ""
        response1 = self.app_client.post('/api/v1/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result1 = json.loads(response1.data)
        self.assertEqual(result1["message"], "Please fill in required email field then try again!")
        self.assertEqual(response1.status_code, 400) 

        #test with empty name
        self.sample_user['email'] = "bob@example.com"
        self.sample_user['name'] = ""
        response2 = self.app_client.post('/api/v1/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result2 = json.loads(response2.data)
        self.assertEqual(result2["message"], "Please fill in required names field then try again!")
        self.assertEqual(response2.status_code, 400)  

        #test with empty email
        self.sample_user['name'] = "Bob Burgers"
        self.sample_user['email'] = ""
        response3 = self.app_client.post('/api/v1/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result3 = json.loads(response3.data)
        self.assertEqual(result3["message"], "Please fill in required password field then try again!")
        self.assertEqual(response3.status_code, 400)        

    def test_signup_invalid_email(self):
        """ Test if user signup is done using an invalid email address"""
        self.sample_user['email'] = "bob@232"
        response = self.app_client.post('/api/v1/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please provide a valid email address!")
        self.assertEqual(response.status_code, 400)  

    def test_signup_invalid_fields(self):
        """ Test for non string input for name and email 
            A name cannot start with anything other than a letter
            A name cannot contail alpha-numeric characters other than ' or -

        """
        #test invalid name
        self.sample_user['name'] = "$Bob &Burgers"
        response = self.app_client.post('/api/v1/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please provide a valid name!")
        self.assertEqual(response.status_code, 400) 

        #test invalid email
        self.sample_user['name'] = "Bob Burgers"
        self.sample_user['email'] = "1bob@example.com"
        response = self.app_client.post('/api/v1/auth/register/', 
                                    data=json.dumps(self.sample_user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["error"], "Please provide a valid email address!")
        self.assertEqual(response.status_code, 400)  
    # end tests for api user signup

if __name__ == "__main__":
    unittest.main()