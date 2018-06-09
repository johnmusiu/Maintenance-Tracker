"""
 defines the endpoints of the API
"""
import os
from flask_api import FlaskAPI
from instance.config import app_config


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv('SECRET_KEY')

    from api.auth.views import auth
    app.register_blueprint(auth)

    from api.mrequests.views import mrequests
    app.register_blueprint(mrequests)

    from api.mrequests.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
