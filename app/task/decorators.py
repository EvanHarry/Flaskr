from flask import abort, g
from functools import wraps

from ..models import Task


def user_only(f):
    @wraps(f)
    def decorated_function(task_id, *args, **kwargs):
        task = Task.query.get(task_id)
        if task.user_id != g.current_user.id:
            abort(401)
        return f(task_id, *args, **kwargs)

    return decorated_function
