#app/auth/views.py

from . import auth
from flask import request, jsonify, json
from api.models import User, Request
import re

@auth.route('/register', methods=['POST'])
def register():
    """ endpoint for user registration """
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    confirm_password = str(request.data.get('confirm_password', ''))

    if not name:
        return jsonify({'message': 'Please fill in required name field!'}), 400
    elif not name.replace(" ", "").isalpha():
        return jsonify({
            'message': "Please enter a valid name!",
            'info': "A valid name has letters and spaces"
        }), 400
    if not email:
        return jsonify({'message': 'Please fill in required email field!'}), 400
    elif not re.match(r"(^[a-zA-Z_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.][a-zA-Z]+$)", email):
        return jsonify({
            'message': 'Please enter a valid email address!'
        }), 400

    if not password:
        return jsonify({
            'message': 'Please fill in required password field!'
            }), 400
    elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}", password):
        return jsonify({
            'message': 'Please enter a strong password to signup!',
            'info': 'Password must contain uppercase and lowercase letters, digits and be have min-lenght of 6'
        }), 400
    if not confirm_password:
        return jsonify({
            'message': 'Please fill in required confirm_password field!'
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
    }), 201

@auth.route('/login', methods=['POST'])
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
            'message': 'Please enter a valid email address!'
        })
        response.status_code = 400
        return response
    if not password:
        response = jsonify({'message': 'Please fill in the password field'})
        response.status_code = 400
        return response
    user = User.users.get(email, False)
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
