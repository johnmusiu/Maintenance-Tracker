"""
This module include tests to the users/requests endpoints of the API

"""

import unittest
import json
from api import create_app
from migration import migration
from api.models import User
from migration import migration


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
		self.app = create_app(config_name="testing")
		self.app_client = self.app.test_client
		self.sample_user = {
			"first_name": "Bob",
			"last_name": "Burgers",
			"email": "bob@example.com",
			"password": "pass@#4W",
			"confirm_password": "pass@#4W"
    	}
		self.sample_user2 = {
			"first_name": "Joan",
			"last_name": "Makena",
			"email": "joan@example.com",
			"password": "pass@#4W",
			"confirm_password": "pass@#4W"
		}

		self.sample_request = {
			"title": "Fix mouses",
			"description": "mouses in lab 2 not working",
			"status": "open",
			"type": "Maintenance",
		}


	def get_header(self):
		""" helper method to generate token """
		response = self.app_client().post('/api/v1/auth/register',
											data=json.dumps(self.sample_user),
											content_type="application/json")
		self.assertEqual(response.status_code, 201)

		response = self.app_client().post('/api/v1/auth/login',
										data=json.dumps(self.sample_user),
										content_type="application/json")
		result = json.loads(response.data)
		access_token = result['access-token']
		return {'access-token': access_token}

	# test unauthorised requests
	def test_no_token(self):
		"""
			Test requests endpoint if user provides not token
		"""
		response = self.app_client().get('/api/v1/users/requests',
										content_type='application/json')
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Token is missing! Login to get token.")
		self.assertEqual(response.status_code, 401)

	# begin tests for api create request
	def test_api_can_create_request(self):
		"""
			Test API make maintenance request with all
			details provided correctly
		"""
		headers = self.get_header()
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Maintenance request submitted successfully.")
		self.assertIn("Fix mouses", str(result))
		self.assertEqual(response.status_code, 201)

	def test_create_request_with_null_field(self):
		"""
			test whether null input raises error for fields
			title/description/type
		"""
		headers = self.get_header()
	
		# test for null title
		self.sample_request['title'] = ""
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Please fill in the 'title' field.")
		self.assertEqual(response.status_code, 400)
	
		# test for null description
		self.sample_request['title'] = "Fix mouses"
		self.sample_request['description'] = ""
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Please fill in the 'description' field.")
		self.assertEqual(response.status_code, 400)
	
		# test for null request type
		self.sample_request['description'] = "mouses in lab 2 not working"
		self.sample_request['type'] = ""
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"], "Please fill in the 'type' field.")
		self.assertEqual(response.status_code, 400)

	def test_create_request_with_invalid_type(self):
		"""
			test that using a type other than maintenance or repair
			returns a value error
		"""
		headers = self.get_header()
	
		self.sample_request['type'] = "Another type"
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Type can only be Maintenance or Repair.")
		self.assertEqual(response.status_code, 400)
	# end tests for api create task
	
	# begin tests for api update request
	def test_api_can_update_request(self):
		""" test user can update a request that is not resolved """
		headers = self.get_header()
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type='application/json',
										headers=headers)
		self.assertEqual(response.status_code, 201)
		result = json.loads(response.data)
		# update values on data to be submitted
		self.sample_request['title'] = "Fix mouses and keyboards"
		self.sample_request['description'] =\
			"Mouses and keyboards in lab 2 not working"
		response1 = self.app_client().put('/api/v1/users/requests/{}'.
										format(result.get('request_id')),
										data=json.dumps(self.sample_request),
										content_type='application/json',
										headers=headers)

		result1 = json.loads(response1.data)
		self.assertEqual(result1["title"], "Fix mouses and keyboards")
		self.assertEqual(result1["message"],
						"Maintenance request updated successfully.")
		self.assertEqual(response1.status_code, 200)

	def test_update_request_with_null_field(self):
		"""
			test whether null input raises error for fields
			title/description/type
		"""
		headers = self.get_header()
		# insert request
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(response.status_code, 201)

		# test for null title
		self.sample_request['title'] = ""
		response = self.app_client().put('/api/v1/users/requests/1',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Please fill in the 'title' field.")
		self.assertEqual(response.status_code, 400)

		# test for null description
		self.sample_request['title'] = "Fix mouses"
		self.sample_request['description'] = ""
		response = self.app_client().put('/api/v1/users/requests/1',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Please fill in the 'description' field.")
		self.assertEqual(response.status_code, 400)

		# test for null request type
		self.sample_request['description'] = "mouses in lab 2 not working"
		self.sample_request['type'] = ""
		response = self.app_client().put('/api/v1/users/requests/1',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"], "Please fill in the 'type' field.")
		self.assertEqual(response.status_code, 400)

	def test_update_request_with_invalid_type(self):
		"""
			test that using a type other than maintenance or repair
			returns a value error
		"""
		headers = self.get_header()
		self.sample_request['type'] = "Another type"
		response = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type="application/json",
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(result["message"],
						"Type can only be Maintenance or Repair.")
		self.assertEqual(response.status_code, 400)
	# end tests for update request

	# begin tests for api get request by id
	def test_api_can_get_request_by_id(self):
		"""
			test that one request can be retrieved if it exists
			test that a suitable message is returned if a requested
			id doesn't exists
		"""
		headers = self.get_header()
		# test fetching a request entry that doesn't exist
		response = self.app_client().get('/api/v1/users/requests/1',
										data=json.dumps(self.sample_request),
										content_type='application/json',
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(response.status_code, 404)
		self.assertIn(result["message"], "Request id not found.")

		# add request, and try to fetch request id 1
		response1 = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(self.sample_request),
										content_type='application/json',
										headers=headers)
		self.assertEqual(response1.status_code, 201)
		result = json.loads(response1.data)
		print({'res1': result})
		response2 = self.app_client().get('/api/v1/users/requests/{}'.
										format(result.get('request_id')),
										headers=headers)
		result2 = json.loads(response2.data)
		print({'res2': result2})
		self.assertEqual(response2.status_code, 200)
		self.assertEqual(result2["title"], "Fix mouses")
	# end tests for api get request by id

	# begin tests for api get all requests
	def test_api_can_get_all_requests(self):
		"""
			test that if user has requests, api can retrieve them
			test that if user has no requests a suitable response is returned
		"""
		headers = self.get_header()
		# test fetching a requests for user who has not submited any requests
		response = self.app_client().get('/api/v1/users/requests',
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(result["message"],
						"You have not made any requests yet!")

		# insert request
		response1 = self.app_client().post('/api/v1/users/requests',
										data=json.dumps(
											self.sample_request),
										content_type='application/json',
										headers=headers)
		self.assertEqual(response1.status_code, 201)

		response = self.app_client().get('/api/v1/users/requests',
										headers=headers)
		result = json.loads(response.data)
		self.assertEqual(response.status_code, 200)
		self.assertIn("Fix mouses", str(result))
		# end tests for api get all requests

  	def tearDown(self):
		""" teardown all initialized variables """
		migration()


if __name__ == "__main__":
  unittest.main()
