# api/requests/super_admin.py

from . import super_admin_bp
from flask import jsonify, request
from ..wrappers import token_required, role_required
from ..auth.views import register_validation
from ..models import SuperAdmin

@super_admin_bp.route('', methods=['POST'])
@token_required
@role_required('2')
def create_admin():
    # create admin
    fname = str(request.data.get('first_name', ''))
    lname = str(request.data.get('last_name', ''))
    email = str(request.data.get('email', ''))
    password = str(request.data.get('password', ''))
    confirm_pass = str(request.data.get('confirm_password', ''))

    # return True is user input is valid
    validation = register_validation(fname, lname, email, password, confirm_pass)

    if validation is not True:
        return validation

    results = SuperAdmin().create(fname, lname, email, password)

    if results[0] is False:
        return jsonify({"message": results[1]}), 409
    else:
        return jsonify({
            'message': "Admin created successfully"
        }), 201
