from sqlalchemy import func, text, null

from utils import db


class Project(db.Model):

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True, server_default=null())
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    pending_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
    completed_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
    on_hold_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
    total_tasks = db.Column(db.Integer, nullable=False, server_default=text('0'))
