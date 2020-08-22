from utils import db


class User(db.Model):
    """User Model"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    projects = db.relationship('Project', secondary="project_owner", backref="owners")
    permissions = db.relationship('Permission', secondary='user_permission', backref='users')
