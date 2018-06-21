# api/super_admin/__init__.py

from flask import Blueprint

super_admin_bp =  Blueprint('super_admin', __name__, url_prefix='/api/v2/admin')

from . import super_admin
