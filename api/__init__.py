"""
 defines the endpoints of the API
"""
from flask_api import FlaskAPI
from flask import request, jsonify, json, abort
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
            result = request_obj.save(1)
            
            if result[0] == "1":
                response = jsonify({
                    'message': "Maintenance request submitted successfully.",
                    'title': title,
                    'description': description,
                    'category': category,
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
    return app
