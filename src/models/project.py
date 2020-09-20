from sqlalchemy import func, text, null

from utils import db


class Project(db.Model):

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False, server_default='')
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status', backref='projects')
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship('Organisation', backref='projects')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_creator = db.relationship('User', backref='projects_created_by')
    project_users = db.relationship('User', backref='user_projects', secondary='user_project')


class ProjectMetrics(db.Model):

    __tablename__ = 'project_metrics'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='metric', uselist=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    status = db.relationship('Status', backref='metrics')
    count = db.Column(db.Integer, nullable=False, server_default=text('0'))


class ProjectRemarksHistory(db.Model):

    __tablename__ = 'project_history'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='remarks')
    remarks = db.Column(db.Text, nullable=True, server_default=null())
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='project_remarks')
