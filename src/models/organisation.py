from sqlalchemy import func

from utils import db


class Organisation(db.Model):

    __tablename__ = 'organisation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False, unique=True)
    passcode = db.Column(db.Text, nullable=False)
    location = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    registered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    registered_by_user = db.relationship('User', backref='org_reg_by', uselist=False)
