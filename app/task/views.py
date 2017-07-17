from flask import jsonify, abort, request, g

from . import task_blueprint
from .. import db
from ..auth import auth
from ..decorators import admin_required
from ..models import Task
from .decorators import user_only


@task_blueprint.route('/tasks', methods=['GET'])
@auth.login_required
@admin_required
def get_tasks():
    tasks = Task.query.all()
    return jsonify({'tasks': [task.to_simple_json() for task in tasks]})


@task_blueprint.route('/tasks/<task_id>', methods=['GET'])
@auth.login_required
@user_only
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if task.user_id != g.current_user.id:
        abort(401)
    return jsonify({'task': task.to_json()})


@task_blueprint.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    data = request.get_json()
    if data is None or not data.keys() >= {'title', 'description'}:
        abort(400)
    task = Task(title=data['title'], description=data['description'], user=g.current_user)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json()), 201


@task_blueprint.route('/tasks/<task_id>', methods=['DELETE'])
@auth.login_required
@user_only
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'task deleted'}), 200


@task_blueprint.route('/tasks/<task_id>', methods=['PUT'])
@auth.login_required
@user_only
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if data is None:
        abort(400)
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.add(task)
    return jsonify({'task': task.to_json()}), 200
