#api/auth/__init__.py
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v2/auth')

from . import auth