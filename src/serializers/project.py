from marshmallow import fields, validate

from utils.serializer import CamelCaseSchema


class CreateProjectSerializer(CamelCaseSchema):
    """Serializer for Creating a Project"""

    name = fields.Str(required=True, validate=[validate.Length(min=3, max=100)])
    description = fields.Str(required=False)
