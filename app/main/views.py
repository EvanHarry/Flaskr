from flask import request, abort, jsonify

from . import main
from ..models import User


@main.route('/token', methods=['POST'])
def generate_token():
    if not request.json or 'username' and 'password' not in request.json:
        abort(400)
    user = User.query.filter_by(username=request.json['username']).first()
    if not user.verify_password(request.json['password']):
        abort(401)
    token = user.generate_auth_token(expiration=3600)
    return jsonify({'token': token})
