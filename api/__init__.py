"""
 defines the endpoints of the API
"""
from flask_api import FlaskAPI
from instance.config import app_config
import re

def create_app(config_name):
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from api.auth.views import auth
    app.register_blueprint(auth)

    from api.mrequests.views import mrequests
    app.register_blueprint(mrequests)

    return app
