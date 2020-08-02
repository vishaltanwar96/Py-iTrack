from utils import db

project_owner_table = db.Table(
    'project_owner',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
)
