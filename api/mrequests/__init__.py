# api/requests/__init__.py

from flask import Blueprint

mrequests = Blueprint('mrequests', __name__, url_prefix='/api/v1/users/requests')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/requests')
super_admin_bp =  Blueprint('super_admin', __name__, url_prefix='/api/v1/admin')

from . import views, admin, super_admin
