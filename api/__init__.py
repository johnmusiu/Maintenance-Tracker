"""
 defines the endpoints of the API
"""
import os
from flask_api import FlaskAPI
from flask_cors import CORS
from instance.config import app_config


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv('SECRET_KEY')

    from api.auth.auth import auth
    app.register_blueprint(auth)

    from api.mrequests.mrequests import mrequests
    app.register_blueprint(mrequests)

    from api.admin.admin import admin_bp
    app.register_blueprint(admin_bp)

    from api.super_admin.super_admin import super_admin_bp
    app.register_blueprint(super_admin_bp)

    return app
