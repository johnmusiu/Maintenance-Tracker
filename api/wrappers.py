from flask import session, jsonify, request
from functools import wraps
import jwt
import os


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('access-token', '')
        if not token:
            return jsonify({
                'message': 'Token is missing! Login to get token.'
            }), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
            session['user_id'] = data.get('user_id')
            session['role'] = data.get('role')

        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session['role'] not in roles:
                return jsonify({
                    'message': u'Access Denied.'
                }), 403
            return f(*args, **kwargs)
        return wrapped
    return wrapper
