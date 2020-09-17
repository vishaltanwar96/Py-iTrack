from operator import itemgetter

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
