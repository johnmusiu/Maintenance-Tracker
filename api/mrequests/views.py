#api/requests/views.py

from . import mrequests
from flask import request, jsonify, json
from api.models import User, Request
import re

@mrequests.route('/requests', methods=['POST', 'GET'])
def requests():
    if request.method == "POST":
        title = str(request.data.get('title', ''))
        description = str(request.data.get('description', ''))
        category = str(request.data.get('type', ''))
        #returns True if user input is valid and meets expectations
        validation = validate_input(title, description, category)
        if validation is not True:
            return validation
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

def validate_input(title, description, category):
    """ validate create or update request user input """
    if not title or not description or not category:
        if not title:
            response = jsonify({
                "message": "Please fill in the 'title' field."
            })
            
        if not description: 
            response = jsonify({
                "message": "Please fill in the 'description' field."
            })
           
        if not category:
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

@mrequests.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    """ endpoint for update request """
    title = str(request.data.get('title', ''))
    description = str(request.data.get('description', ''))
    category = str(request.data.get('type', ''))

    # return True is user input is valid
    validation = validate_input(title, description, category)
    if validation is not True:
        return validation

    results = Request().update(1, request_id, title, description, category)
    if results[0] == "0":
        return jsonify({"message": results[1]}), 404
    else:
        result = results[1]
        result = result.get(title)

        return jsonify({
            "message": "Maintenance request updated successfully.",
            "request_id": result[0],
            "title": result[1],
            "description": result[2],
            "type": result[3],
            "user_id": result[4],
            "status": result[5],
            "created_at": result[6],
            "updated_at": result[7]
        }), 200

@mrequests.route('/requests/<int:request_id>', methods=['GET'])
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
