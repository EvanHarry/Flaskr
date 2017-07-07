from flask import request, abort, jsonify

from . import main_blueprint
from ..models import User


@main_blueprint.route('/token', methods=['POST'])
def generate_token():
    data = request.get_json()
    if data is None or not data.keys() >= {'username', 'password'}:
        abort(400)
    user = User.query.filter_by(username=data.get('username')).first()
    if user is None:
        abort(404)
    if not user.verify_password(data.get('password')):
        abort(401)
    token = user.generate_auth_token(expiration=3600)
    return jsonify({'token': token})
