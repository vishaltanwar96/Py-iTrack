from marshmallow import fields, validate, Schema

from utils import ma
from models import Project


class CreateProjectSerializer(Schema):
    """Serializer for Creating a Project"""

    name = fields.Str(required=True, validate=[validate.Length(min=3, max=100)])
    description = fields.Str(required=False)


class ProjectSerializer(ma.SQLAlchemyAutoSchema):
    """Serializer for dumping project details"""

    class Meta:
        """."""

        model = Project
        incude_fk = True
