from flask import jsonify, abort, request

from . import user_blueprint
from .. import db
from ..auth import auth
from ..decorators import admin_required
from ..models import User


@user_blueprint.route('/users', methods=['GET'])
@auth.login_required
@admin_required
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_simple_json() for user in users]})


@user_blueprint.route('/users/<user_id>', methods=['GET'])
@auth.login_required
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return jsonify({'user': user.to_json()})


@user_blueprint.route('/users', methods=['POST'])
@auth.login_required
@admin_required
def create_user():
    if not request.json or 'username' and 'password' not in request.json:
        abort(400)
    users = User.query.filter_by(username=request.json['username']).first()
    if users is not None:
        abort(400)
    if 'admin' not in request.json:
        admin = False
    else:
        admin = request.json['admin']
    user = User(username=request.json['username'], password=request.json['password'], admin=admin)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user deleted'}), 200


@user_blueprint.route('/users/<user_id>', methods=['PUT'])
@auth.login_required
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400)
    user.admin = request.json.get('admin', user.admin)
    db.session.add(user)
    return jsonify({'user': user.to_json()}), 200
