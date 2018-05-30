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
                    "message": "Please fill in 'title' field"
                })
                response.status_code = 400
                return response
            if not description: 
                response = jsonify({
                    "message": "Please fill in 'description' field"
                })
                response.status_code = 400
                return response
            if not category:
                response = jsonify({
                    "message": "Please fill in 'type' field"
                })
                response.status_code = 400
                return response
            if category not in ['maintenance', 'repair']:
                response = jsonify({
                    "message": "Please provide a valid request type"
                })
                response.status_code = 400
                return response
            
            request_obj = Request(title, description, category)
            request_obj.save()
            response = jsonify({
                'title': title,
                'description': description,
                'category': category,
            })
            response.status_code = 201
        else:
            return jsonify({"message": "get requests"})

    return app
