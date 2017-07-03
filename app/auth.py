from flask import make_response, jsonify, g
from flask_httpauth import HTTPTokenAuth

from .models import User

auth = HTTPTokenAuth('Bearer')


@auth.verify_token
def verify_token(token):
    if token == '':
        return None
    g.current_user = User.verify_auth_token(token)
    return g.current_user is not None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized'}), 401)
