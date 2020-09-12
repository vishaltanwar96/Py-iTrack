from sqlalchemy import text, func

from utils import db


class User(db.Model):
    """User Model"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    is_verified = db.Column(db.Boolean, server_default=text('0'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref='users')
