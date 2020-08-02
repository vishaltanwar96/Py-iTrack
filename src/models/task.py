from sqlalchemy import null, func

from utils import db


class Task(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True, server_default=null())
    remarks = db.Column(db.Text, nullable=True, server_default=null())
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_by = db.relationship('User', foreign_keys=[assigned_by_id])
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    criticality_id = db.Column(db.Integer, db.ForeignKey('criticality.id'))
    criticality = db.relationship('Criticality', backref='tasks')
    status = db.relationship('Status', backref='tasks')
    expected_closure_by = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref='tasks')
