"""
 defines the endpoints of the API
"""
from flask_api import FlaskAPI
from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify, json, abort
from instance.config import app_config
import re
import jwt

def create_app(config_name):
    from api.app.models import Request, User, users
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route('/api/v1/auth/register', methods=['POST'])
    def register():
        """ endpoint for user registration """
        name = str(request.data.get('name', ''))
        email = str(request.data.get('email', ''))
        password = str(request.data.get('password', ''))
        confirm_password = str(request.data.get('confirm_password', ''))

        if not name:
            return jsonify({'message': 'Please fill in the "name" field'}), 400
        if not email:
            return jsonify({'message': 'Please fill in the "email" field'}), 400
        elif not re.match(r"(^[a-zA-Z_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.][a-zA-Z]+$)", email):
            return jsonify({
                'message': 'Please enter a valid email address'
            }), 400

        if not password:
            return jsonify({
                'message': 'Please fill in the "password" field'
                }), 400
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}", password):
            return jsonify({
                'message': 'Password must contain uppercase and lowercase letters, digits and be have min-lenght of 6'
            }), 400
        if not confirm_password:
            return jsonify({
                'message': 'Please fill in the "confirm_password" field'
                }), 400
        if password != confirm_password:
            return jsonify({
                'message': 'Password and confirm password mismatch'
            }), 400
        # now save user to db
        user = User(name, email, password)
        result = user.signup()
        if result[0] == "0":
            return jsonify({
                'message': result[1]
            }), 400
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': result[1][0],
            'email': result[1][1],
            'name': result[1][2]
        })

    @app.route('/api/v1/auth/login', methods=['POST'])
    def login():
        """ define user login and token issuance """
        email = str(request.data.get('email', ''))
        password = str(request.data.get('password', ''))

        if not email:
            response = jsonify({'message': 'Please fill in the email field'})
            response.status_code = 400
            return response
        elif not re.match(r"(^[a-zA-Z_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.][a-zA-Z]+$)", email):
            response =  jsonify({
                'message': 'Please enter a valid email address'
            })
            response.status_code = 400
            return response
        if not password:
            response = jsonify({'message': 'Please fill in the password field'})
            response.status_code = 400
            return response
        
        user = users.get(email, False)
        if user is False:
            return jsonify({
                'message': "User account not found!"
            })
        else:
            current_user = User(user[1], user[3], user[2])
            if current_user.verify_password(password):
                token = current_user.generate_token(current_user.email)
                return jsonify({
                    'message': 'Login successful, welcome!',
                    # 'access_token': token.decode(),
                    'email': email
                }), 200
            else:
                return jsonify({
                    'message': "Wrong login credentials provided!"
                }), 202
 

    @app.route('/api/v1/users/requests', methods=['POST', 'GET'])
    def requests():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            description = str(request.data.get('description', ''))
            category = str(request.data.get('type', ''))
            if not title:
                response = jsonify({
                    "message": "Please fill in the 'title' field."
                })
                response.status_code = 400
                return response
            if not description: 
                response = jsonify({
                    "message": "Please fill in the 'description' field."
                })
                response.status_code = 400
                return response
            if not category:
                response = jsonify({
                    "message": "Please fill in the 'type' field."
                })
                response.status_code = 400
                return response
            if category not in ['maintenance', 'repair']:
                response = jsonify({
                    "message": "Type can only be Maintenance or Repair."
                })
                response.status_code = 400
                return response
            
            request_obj = Request(title, description, category)
            results = request_obj.save(1)
            
            if results[0] == "1":
                result = results[1].get(title)
                response = jsonify({
                    'message': "Maintenance request submitted successfully.",
                    'request_id': result[0],
                    'title': title,
                    'description': result[1],
                    'type': result[2],
                    'status': result[4],
                    'user_id': result[3],
                    'created_at': result[5],
                    'updated_at': result[6],
                })
                response.status_code = 201
            else:
                response = jsonify({
                    "message": "Duplicate request, request not saved"
                })
                response.status_code = 202
            return response
        elif request.method == "GET":
            #returns all requests made by a certain user
            result = Request().get_all_my_requests(1)
            if result == "0":
                return jsonify(
                        {"message": "You have not made any requests yet!"}), 404
            response = json.dumps(result[1])
            return response, 200

    @app.route('/api/v1/users/requests/<int:request_id>', methods=['PUT'])
    def update_request(request_id):
        """ endpoint for update request """
        title = str(request.data.get('title', ''))
        description = str(request.data.get('description', ''))
        category = str(request.data.get('type', ''))
        if not title:
            response = jsonify({
                "message": "Please fill in the 'title' field."
            })
            response.status_code = 400
            return response
        if not description: 
            response = jsonify({
                "message": "Please fill in the 'description' field."
            })
            response.status_code = 400
            return response
        if not category:
            response = jsonify({
                "message": "Please fill in the 'type' field."
            })
            response.status_code = 400
            return response
        if category not in ['maintenance', 'repair']:
            response = jsonify({
                "message": "Type can only be Maintenance or Repair."
            })
            response.status_code = 400
            return response
        results = Request().update(1, request_id, title, description, category)
        if results[0] == "0":
            return jsonify({"message": results[1]}), 404
        else:
            result = results[1]

            return jsonify({
                "message": "Request updated successfully",
                "request_id": result[0],
                "title": result[1],
                "description": result[2],
                "type": result[3],
                "user_id": result[4],
                "status": result[5],
                "created_at": result[6],
                "updated_at": result[7]
            }), 200

    @app.route('/api/v1/users/requests/<int:request_id>', methods=['GET'])
    def get_request_by_id(request_id):
        """ route to retrieve request by id """
        result = Request().get_by_id(1, request_id)
        
        if result[0] == "0":
            return jsonify({"message": "Request id not found."}), 404
        response = jsonify({
            "message":"Request id found.",
            "request_id": result[2][0],
            "title": result[1],
            "description": result[2][1],
            "status": result[2][4],
            "user_id": result[2][3],
            "type": result[2][2],
            "created_at" : result[2][5]
        })
        return response, 200


    return app
