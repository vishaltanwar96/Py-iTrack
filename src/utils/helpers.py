from functools import wraps
from operator import itemgetter

from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_current_user

from models import Role, User
from .misc_instances import db, jwt


def get_super_users():
    """Get Admin & Manager Role id"""

    return tuple(
        map(itemgetter(0), db.session.query(Role.id).filter(Role.value.in_(('ADMIN', 'MANAGER'))).all())
    )


@jwt.user_loader_callback_loader
def load_current_user(identity):
    """:returns user instance loaded from current identity of the protected route"""

    if not identity:
        return None
    return User.query.get(identity)


def super_users_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if get_current_user().role_id in get_super_users():
            return func(*args, **kwargs)
        else:
            return jsonify({'status': False, 'msg': 'Action not permissible', 'data': None}), 403

    return wrapper


def verify_json_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({'status': False, 'msg': 'Invalid JSON', 'data': None}), 400
        return func(*args, **kwargs)

    return wrapper
