# api/requests/admin.py

from . import admin
from flask import request, jsonify, session
from api.models import Request
from ..wrappers import token_required, role_required

@admin.route('', methods=['GET'])
@token_required
@role_required('1')
def requests():
    # returns all requests
    result = Request().admin_get_all()
    if result is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result)
    return response, 200

@admin.route('/<int:request_id>', methods=['GET'])
@token_required
@role_required('1')
def request_by_id(request_id):
    # returns all requests
    result = Request().admin_get_by_id(request_id)
    if result is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200

@admin.route('/<int:request_id>/approve', methods=['PUT'])
@token_required
@role_required('1')
def approve(request_id):
    # returns all requests
    result = Request().admin_approve(request_id)
    if result is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200

@admin.route('/<int:request_id>/disapprove', methods=['PUT'])
@token_required
@role_required('1')
def disapprove(request_id):
    # returns all requests
    result = Request().admin_disapprove(request_id)
    if result is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200

@admin.route('/<int:request_id>/resolve', methods=['PUT'])
@token_required
@role_required('1')
def resolve(request_id):
    # returns all requests
    result = Request().admin_resolve(request_id)
    if result is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200
