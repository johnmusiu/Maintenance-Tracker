# api/requests/admin.py

from . import admin_bp
from flask import jsonify
from api.models import Admin
from ..wrappers import token_required, role_required


@admin_bp.route('', methods=['GET'])
@token_required
@role_required('1')
def requests():
    # returns all requests
    result = Admin().get_all_requests()
    if result[0] is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200


@admin_bp.route('/<int:request_id>', methods=['GET'])
@token_required
@role_required('1')
def request_by_id(request_id):
    # returns all requests
    result = Admin().get_request_by_id(request_id)
    if result[0] is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200


@admin_bp.route('/<int:request_id>/approve', methods=['PUT'])
@token_required
@role_required('1')
def approve(request_id):
    # returns all requests
    result = Admin().approve(request_id)
    if result[0] is False:
        return jsonify(
            {"message": result[1]}), result[2]
    response = jsonify(result[1])
    return response, 200


@admin_bp.route('/<int:request_id>/disapprove', methods=['PUT'])
@token_required
@role_required('1')
def disapprove(request_id):
    # returns all requests
    result = Admin().disapprove(request_id)
    if result[0] is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200


@admin_bp.route('/<int:request_id>/resolve', methods=['PUT'])
@token_required
@role_required('1')
def resolve(request_id):
    # returns all requests
    result = Admin().resolve(request_id)
    if result[0] is False:
        return jsonify(
            {"message": "There are no requests yet!"}), 404
    response = jsonify(result[1])
    return response, 200
