# api/requests/__init__.py

from flask import Blueprint

mrequests = Blueprint('mrequests', __name__, url_prefix='/api/v2/users/requests')

from . import mrequests
