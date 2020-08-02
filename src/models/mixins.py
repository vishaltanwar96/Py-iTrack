from utils import db


class IdValueMixin(object):
    """."""

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), nullable=False, unique=True)
