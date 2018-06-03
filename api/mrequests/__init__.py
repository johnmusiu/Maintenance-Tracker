#api/requests/__init__.py

from flask import Blueprint

mrequests = Blueprint('mrequests', __name__)

from . import views