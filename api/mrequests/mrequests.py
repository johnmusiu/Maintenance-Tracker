# api/requests/views.py

from . import mrequests
from flask import request, jsonify, session
from api.models import NormalUser
from ..wrappers import token_required, role_required


@mrequests.route('', methods=['POST', 'GET'])
@token_required
@role_required('0')
def requests():
    if request.method == "POST":
        title = str(request.data.get('title', ''))
        description = str(request.data.get('description', ''))
        category = str(request.data.get('type', ''))
        # returns True if user input is valid and meets expectations
        validation = validate_input(title, description, category)
        if validation is not True:
            return validation
        result = NormalUser().make_request(title, description, category)
        if result[0] is False:
            response = jsonify({
                'message': result[1]
            })
        else:
            response = jsonify({
                'message': "Maintenance request submitted successfully.",
                'request_id': result[1],
                'title': title,
                'description': description,
                'type': category,
                'status': 'open'
            })
            response.status_code = 201
        return response
    elif request.method == "GET":
        # returns all requests made by a certain user
        result = NormalUser().get_requests()
        if result is False:
            return jsonify(
                {"message": "You have not made any requests yet!"}), 404
        response = jsonify(result)
        return response, 200


def validate_input(title, description, category):
    """ validate create or update request user input """
    if not title or not description or not category:
        if not title:
            response = jsonify({
                "message": "Please fill in the 'title' field."
            })

        elif not description:
            response = jsonify({
                "message": "Please fill in the 'description' field."
            })

        elif not category:
            response = jsonify({
                "message": "Please fill in the 'type' field."
            })
        response.status_code = 400
        return response
    else:
        if category not in ['Maintenance', 'Repair']:
            response = jsonify({
                "message": "Type can only be Maintenance or Repair."
            })
            response.status_code = 400
            return response
    return True


@mrequests.route('/<int:request_id>', methods=['PUT'])
@token_required
@role_required('0')
def update_request(request_id):
    """ endpoint for update request """
    title = str(request.data.get('title', ''))
    description = str(request.data.get('description', ''))
    category = str(request.data.get('type', ''))

    # return True is user input is valid
    validation = validate_input(title, description, category)
    if validation is not True:
        return validation

    results = NormalUser().update_request(request_id, title, description, category)
    if results[0] is False:
        return jsonify({"message": results[1]}), results[2]

    return jsonify({
        "message": "Maintenance request updated successfully.",
        "request_id": request_id,
        "title": title,
        "description": description,
        "type": category,
        "user_id": session['user_id'],
        "status": 'open'
    }), 200


@mrequests.route('/<int:request_id>', methods=['GET'])
@token_required
@role_required('0')
def get_request_by_id(request_id):
    """ route to retrieve request by id """
    # returns all requests made by a certain user
    result = NormalUser().get_request_by_id(request_id)
    if result[0] is False:
        return jsonify(
            {"message": result[1]}), result[2]
    response = jsonify(result[1])
    return response, 200
