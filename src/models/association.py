from utils import db

role_permission_table = db.Table(
    'role_permission',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), nullable=False),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), nullable=False),
)

user_organisation_table = db.Table(
    'user_organisation',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('organisation_id', db.Integer, db.ForeignKey('organisation.id'), nullable=False),
)