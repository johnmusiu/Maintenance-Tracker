# api/admin/__init__.py

from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v2/requests')

from . import admin
