from sqlalchemy import null, func, Computed, text

from utils import db


class Task(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by_id = db.relationship('User', foreign_keys=[created_by])
    assigned_by_id = db.relationship('User', foreign_keys=[assigned_by])
    assigned_to_id = db.relationship('User', foreign_keys=[assigned_to])
    reviewed_by_id = db.relationship('User', foreign_keys=[reviewed_by])
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status', backref='tasks')
    criticality_id = db.Column(db.Integer, db.ForeignKey('criticality.id'))
    criticality = db.relationship('Criticality', backref='tasks')
    expected_completion_date = db.Column(
        db.DateTime,
        server_default=Computed(sqltext=text('created_at + INTERVAL 3 DAY'), persisted=True),
        nullable=False
    )
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref='tasks')
    actual_completion_date = db.Column(db.DateTime, server_default=null(), nullable=True)


class TaskRemarksHistory(db.Model):

    __tablename__ = 'task_history'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', backref='remarks')
    remarks = db.Column(db.Text, nullable=True, server_default=null())
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_creator = db.relationship('User', backref='tasks_created')
