from utils import db
from .mixins import IdValueMixin


class Role(db.Model, IdValueMixin):

    __tablename__ = 'role'


class Status(db.Model, IdValueMixin):

    __tablename__ = 'status'

    projects = db.relationship('Project', backref='status')


class Criticality(db.Model, IdValueMixin):

    __tablename__ = 'criticality'
