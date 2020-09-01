from sqlalchemy import func

from utils import db


class Organisation(db.Model):

    __tablename__ = 'organisation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False, unique=True)
    passcode = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(30), nullable=False)
    registered_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    registered_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organisation_registerer = db.relationship('User', backref='organisation_registered', uselist=False)
    user_organisation = db.relationship('Organisation', backref='users', secondary='user_organisation')
