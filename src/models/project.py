from sqlalchemy import func, text, null

from utils import db


class Project(db.Model):

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True, server_default=null())
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship('Organisation', backref='projects')


class ProjectMetrics(db.Model):

    __tablename__ = 'project_metrics'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='metric', uselist=False)
    pending_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
    completed_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
    on_hold_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
    total_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))


class ProjectRemarksHistory(db.Model):

    __tablename__ = 'project_history'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='remarks')
    remarks = db.Column(db.Text, nullable=True, server_default=null())
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='project_remarks')
