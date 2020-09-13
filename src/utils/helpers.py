from operator import itemgetter

from models import Role
from .misc_instances import db


def get_super_users():
    """Get Admin & Manager Role id"""

    return tuple(
        map(itemgetter(0), db.session.query(Role.id).filter(Role.value.in_(('ADMIN', 'MANAGER'))).all())
    )
