from utils import db


user_organisation_table = db.Table(
    'user_organisation',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('organisation_id', db.Integer, db.ForeignKey('organisation.id'), nullable=False),
)