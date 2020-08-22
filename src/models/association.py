from utils import db

project_owner_table = db.Table(
    'project_owner',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
)

user_permission_table = db.Table(
    'user_permission',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
)