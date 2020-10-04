from marshmallow import fields, validate, Schema

from utils import ma
from models import Organisation


class OrganisationSerializer(ma.SQLAlchemyAutoSchema):
    """Serializer for dumping organisation"""

    passcode = fields.Str(load_only=True)

    class Meta:
        """."""

        model = Organisation
        include_fk = True
        exclude = ('passcode',)


class OrganisationRegistrationSerializer(Schema):
    """Schema for registering organisation"""

    name = fields.Str(required=True, validate=[validate.Length(min=1, max=70)])
    passcode = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=40),
            validate.Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                error="""
                            Minimum eight characters, at least one uppercase letter, 
                            one lowercase letter, one number and one special character
                        """
            )
        ]
    )
    location = fields.Str(required=True, validate=[validate.Length(min=1, max=30)])


class ChangeOrganisationSerializer(Schema):
    """Schema for changing organisation information"""

    name = fields.Str(required=False, validate=[validate.Length(min=1, max=70)])
    passcode = fields.Str(
        required=False,
        validate=[
            validate.Length(min=8, max=40),
            validate.Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                error="""
                            Minimum eight characters, at least one uppercase letter, 
                            one lowercase letter, one number and one special character
                        """
            )
        ]
    )
    location = fields.Str(required=False, validate=[validate.Length(min=1, max=30)])
