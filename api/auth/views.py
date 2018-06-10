# app/auth/views.py

from . import auth
from flask import request, jsonify
from api.models import User
import re


@auth.route('/register', methods=['POST'])
def register():
    """ endpoint for user registration """
    fname = str(request.data.get('first_name', ''))
    lname = str(request.data.get('last_name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    confirm_password = str(request.data.get('confirm_password', ''))

    # returns True if all fields are properly filled
    validation = register_validation(
        fname, lname, email, password, confirm_password)
    if validation is not True:
        return validation

    # now save user to db
    result = User().signup(fname, lname, email, password)

    if result[0] is False:
        return jsonify({
            'message': result[1]
        }), 409

    return jsonify({
        'message': 'Registration successfull',
        'email': result[1],
        'name': result[2] + " " + result[3],
    }), 201


def register_validation(fname, lname, email, password, confirm_password):
    """ function to check if user fills in required data on sign up """
    response = True
    # call login validate as it validates some similar fields
    response = login_validation(email, password)
    if response is not True:
        return response

    # check for null fields
    if not fname or not lname or not confirm_password:
        if not fname:
            response = jsonify({
                'message': 'Please fill in required first_name field!'
            })
        if not lname:
            response = jsonify({
                'message': 'Please fill in required last_name field!'
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
        if not fname.isalpha():
            response = jsonify({
                'message': "Please enter a valid first_name!",
                'first_name': "A valid name has only letters and no spaces."
            })
        if not lname.isalpha():
            response = jsonify({
                'message': "Please enter a valid name!",
                'last_name': "A valid name has only letters and no spaces."
            })

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}", password):
            response = jsonify({
                'message': 'Please enter a strong password to signup!',
                'pasword': """Password must contain uppercase and lowercase letters,
                        digits and be have min-lenght of 6"""
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


@auth.route('/login', methods=['POST'])
def login():
    """ define user login and token issuance """
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))

    # return True if valid sign in data provided
    validation = login_validation(email, password)
    if validation is not True:
        return validation

    user = User().signin(email, password)

    if user is False:
        return jsonify({
            'message': "Wrong login credentials provided!"
        }), 202
    else:
        token = User().generate_token(email, user['is_admin'], user['id'])
        return jsonify({
            'message': 'Login success, welcome!',
            'access-token': token.decode(),
        }), 200


def login_validation(email, password):
    """ method to validate login user provided data """
    if not email:
        response = jsonify({'message': 'Please fill in required email field!'})
        response.status_code = 400
        return response
    elif not re.match(r"(^[a-zA-Z_][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.][a-zA-Z]+$)", email):
        response = jsonify({
            'message': 'Please enter a valid email address!'
        })
        response.status_code = 400
        return response
    if not password:
        response = jsonify(
            {'message': 'Please fill in required password field!'})
        response.status_code = 400
        return response

    return True
