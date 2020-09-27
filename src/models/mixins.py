from utils import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import func, null


class IdValueMixin(object):
    """."""

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), nullable=False, unique=True)


class HistoryMixin(object):
    """."""

    remarks = db.Column(db.Text, nullable=True, server_default=null())
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
