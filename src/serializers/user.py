from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, post_load, fields, validate

from models.user import User
from utils.misc_instances import ma


class UserRegistrationSerializer(Schema):
    """Validation And De-serialization For User Registration"""

    first_name = fields.Str(required=True, validate=[validate.Length(min=1, max=50)])
    last_name = fields.Str(required=True, validate=[validate.Length(min=1, max=50)])
    email = fields.Email(required=True, validate=[validate.Email()])
    password = fields.Str(
        required=True,
        load_only=True,
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
    role_id = fields.Int(required=True, validate=[validate.Range(min=0, max=1, max_inclusive=True, min_inclusive=True)])

    @post_load
    def make_user(self, data, *args, **kwargs):
        """:returns user instance to be added to database"""

        data['password'] = generate_password_hash(password=data.pop('password'))
        return User(**data)


class UserLoginSerializer(Schema):
    """Login Validation and De-serialization"""

    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def check_user(self, data, *args, **kwargs):
        """Check user existence"""

        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    return user.id
        return None


class UserSerializer(ma.SQLAlchemyAutoSchema):
    """Serializer for User Dumps"""

    password = fields.Str(load_only=True)

    class Meta:
        """."""
        model = User
        include_fk = True


class UserChangeDetailsSerializer(Schema):
    """Serializer to Change User Details"""

    first_name = fields.Str(required=False, validate=[validate.Length(min=1, max=50)])
    last_name = fields.Str(required=False, validate=[validate.Length(min=1, max=50)])
    email = fields.Email(required=False, validate=[validate.Email()])
    password = fields.Str(
        required=False,
        load_only=True,
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
    role_id = fields.Int(required=False, validate=[validate.Range(min=0, max=1, max_inclusive=True, min_inclusive=True)])
