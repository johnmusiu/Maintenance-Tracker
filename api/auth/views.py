#app/auth/views.py

from . import auth
from flask import request, jsonify, json
from api.models import User, Request
import re

@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    """ endpoint for user registration """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    confirm_password = str(request.data.get('confirm_password', ''))
    
    #returns True if all fields are properly filled
    validation = register_validation(name, email, password, confirm_password)

    if validation is not True:
        return validation

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
    }), 201

def register_validation(name, email, password, confirm_password):
    """ function to check if user fills in required data on sign up """
    response = True

    #check for null fields
    if not name or not email or not password or not confirm_password:
        if not name:
            response = jsonify({
                'message': 'Please fill in required name field!'
            })
        if not email:
            response = jsonify({
                'message': 'Please fill in required email field!'
            })
        if not password:
            response = jsonify({
                'message': 'Please fill in required password field!'
            })
        if not confirm_password:
            response = jsonify({
                'message': 'Please fill in required confirm_password field!'
            })
        if response is not True:
            response.status_code = 400
        return response
    # check if provided data is valid
    else:
        if not name.replace(" ", "").isalpha():
            response = jsonify({
                'message': "Please enter a valid name!",
                'info': "A valid name has only letters and spaces."
            })
    
        if not re.match(
                r"(^[a-zA-Z_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.][a-zA-Z]+$)",
                email):
            response = jsonify({
                'message': 'Please enter a valid email address!'
            })
 
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}", password):
            response = jsonify({
                'message': 'Please enter a strong password to signup!',
                'info': 'Password must contain uppercase and lowercase letters,\
                        digits and be have min-lenght of 6'
        })
        if response is not True:
            response.status_code = 400
        return response
    # check if password matches confirm password
    if password != confirm_password:
        response = jsonify({
            'message': 'Password and confirm password mismatch'
        })
        response.status_code = 400
    
    return response
 
@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    """ define user login and token issuance """
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))

    # return True if valid sign in data provided
    validation = login_validation(email, password)
    if validation is not True:
        return validation

    user = User().users.get(email, False)
    if user is False:
        return jsonify({
            'message': "Wrong login credentials provided!"
        }), 202
    else:
        current_user = User(user[1], user[3], user[2])
        if current_user.verify_password(password):
            token = current_user.generate_token(email)
            return jsonify({
                'message': 'Login success, welcome!',
                'access_token': token.decode(),
            }), 200
        else:
            return jsonify({
                'message': "Wrong login credentials provided!"
            }), 202

def login_validation(email, password):
    """ method to validate login user provided data """
    if not email:
        response = jsonify({'message': 'Please fill in the email field'})
        response.status_code = 400
        return response
    elif not re.match(r"(^[a-zA-Z_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.][a-zA-Z]+$)", email):
        response =  jsonify({
            'message': 'Please enter a valid email address!'
        })
        response.status_code = 400
        return response
    if not password:
        response = jsonify({'message': 'Please fill in the password field'})
        response.status_code = 400
        return response
    
    return True