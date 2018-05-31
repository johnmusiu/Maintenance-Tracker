"""
 defines the endpoints of the API
"""
from flask_api import FlaskAPI
from flask import request, jsonify, abort
from instance.config import app_config

def create_app(config_name):
    from api.app.models import Request

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')


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
            return jsonify({"message": "get requests"}) 

    return app
