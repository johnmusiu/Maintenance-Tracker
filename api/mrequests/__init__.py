# api/requests/__init__.py

from flask import Blueprint

mrequests = Blueprint('mrequests', __name__, url_prefix='/api/v1/users/requests')
admin = Blueprint('admin', __name__, url_prefix='/api/v1/requests')


from . import views, admin
