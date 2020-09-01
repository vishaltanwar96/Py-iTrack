from utils import db
from .mixins import IdValueMixin


class Role(db.Model, IdValueMixin):

    __tablename__ = 'role'


class Status(db.Model, IdValueMixin):

    __tablename__ = 'status'


class Criticality(db.Model, IdValueMixin):

    __tablename__ = 'criticality'


class Permission(db.Model, IdValueMixin):

    __tablename__ = 'permission'

# Static Models using Metaclasses
# models = ('role', 'status', 'criticality', 'permission')
#
# for model in models:
#     capitalized_model = model.capitalize()
#     locals()[capitalized_model] = type(
#         capitalized_model,
#         (db.Model, ),
#         {
#             '__tablename__': model,
#             'id': db.Column(db.Integer, primary_key=True),
#             'value': db.Column(db.String(100), nullable=False, unique=True)
#         }
#     )
