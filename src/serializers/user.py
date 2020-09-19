from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import post_load, fields, validate

from models.user import User
from utils.misc_instances import ma
from utils.serializer import CamelCaseSchema


# Todo: Find a way to change the attributes of a field initialized in parent class(DRY CODE).
class UserChangeDetailsSerializer(CamelCaseSchema):
    """Serializer to Change User Details"""

    first_name = fields.Str(required=False, validate=[validate.Length(min=1, max=50)])
    last_name = fields.Str(required=False, validate=[validate.Length(min=1, max=50)])
    email = fields.Email(required=False, validate=[validate.Email()])
    password = fields.Str(
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

    @post_load
    def hash_password(self, data, *args, **kwargs):
        """If PUT request has password changes plain text password to hashed password"""

        if 'password' in data.keys():
            data['password'] = generate_password_hash(password=data.pop('password'))
        return data


# TODO: Find a way to dynamically calculate the count of roles and fill in the max value of Role_id
class UserRegistrationSerializer(CamelCaseSchema):
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
    role_id = fields.Int(
        required=True, validate=[validate.Range(min=1, max=3, max_inclusive=True, min_inclusive=True)]
    )

    @post_load
    def make_user(self, data, *args, **kwargs):
        """:returns user instance to be added to database"""

        data['password'] = generate_password_hash(password=data.pop('password'))
        return User(**data)


class UserLoginSerializer(CamelCaseSchema):
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


class UserSerializer(ma.SQLAlchemyAutoSchema, CamelCaseSchema):
    """Serializer for User Dumps"""

    password = fields.Str(load_only=True)

    class Meta:
        """."""

        model = User
        include_fk = True
        exclude = ('password', )
