from marshmallow import fields, validate

from utils import ma
from models import Project
from utils.serializer import CamelCaseSchema


class CreateProjectSerializer(CamelCaseSchema):
    """Serializer for Creating a Project"""

    name = fields.Str(required=True, validate=[validate.Length(min=3, max=100)])
    description = fields.Str(required=False)


class ProjectSerializer(ma.SQLAlchemyAutoSchema, CamelCaseSchema):
    """Serializer for dumping project details"""

    class Meta:
        """."""

        model = Project
        incude_fk = True
