from flask import views, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_current_user
)

from models import User, Role
from utils.helpers import super_users_only, verify_json_request
from utils.misc_instances import db
from serializers.user import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserChangeDetailsSerializer,
)


class UserController(views.MethodView):
    """User CRUD Views"""

    @verify_json_request
    def post(self, *args, **kwargs):
        """Creates a User (User Registration)"""

        serializer = UserRegistrationSerializer()
        request_data = request.get_json()

        if User.query.filter_by(email=request_data.get('email')).first():
            return jsonify({'status': False, 'msg': 'User already exists', 'data': None}), 400

        if not Role.query.get(request_data['roleId']):
            return jsonify({'status': False, 'msg': 'Role doesn\'t exist', 'data': None}), 404

        try:
            user = serializer.load(request_data)
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': True, 'msg': 'Registration Successful', 'data': {'id': user.id}}), 201
        except ValidationError as err:
            return jsonify({'status': False, 'msg': 'Validations failed', 'errors': err.messages}), 400

    @jwt_required
    def get(self, user_id=None, *args, **kwargs):
        """Get a User or a List of Users"""

        if not user_id:
            users = User.query.all()
            serializer = UserSerializer(many=True)
            return jsonify({'status': False, 'msg': 'Fetched data successfully', 'data': serializer.dump(users)}), 200

        user = User.query.get(user_id)

        if not user:
            return jsonify({'status': False, 'msg': 'User doesn\'t exist', 'data': None}), 404

        serializer = UserSerializer()
        return jsonify({'status': False, 'msg': 'Fetched data successfully', 'data': serializer.dump(user)}), 200

    @jwt_required
    @verify_json_request
    def put(self, *args, **kwargs):
        """Change User Information"""

        user = User.query.filter_by(id=get_jwt_identity())

        if not user.first():
            return jsonify({'status': False, 'msg': 'User doesn\'t exist', 'data': None}), 404

        try:
            request_data = request.get_json()
            serializer = UserChangeDetailsSerializer()
            update_data = serializer.load(request_data)
            user.update(update_data)
            db.session.commit()
            return jsonify(
                {
                    'status': True,
                    'msg': 'Details saved successfully',
                    'data': {'modified_fields': list(request_data.keys())}
                }
            ), 200
        except ValidationError as err:
            return jsonify(
                {'status': False, 'msg': 'Validations Failed', 'errors': err.messages, 'data': None}
            ), 400

    @jwt_required
    @super_users_only
    def delete(self, user_id=None):
        """Deletes a user"""

        if not user_id:
            return jsonify({'status': False, 'msg': 'No user id specified', 'data': None}), 400

        current_user = get_current_user()

        if current_user.id == user_id:
            return jsonify({'status': False, 'msg': 'Action not permissible', 'data': None}), 403

        user_to_delete = User.query.get(user_id)

        if not user_to_delete:
            return jsonify({'status': False, 'msg': 'Invalid user id, not found', 'data': None}), 404

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({'status': False, 'msg': 'User successfully deleted', 'data': {'id': user_id}}), 200


class UserLoginController(views.MethodView):
    """User Login"""

    @verify_json_request
    def post(self, *args, **kwargs):
        """Handle User Login"""

        serializer = UserLoginSerializer()

        try:
            user_id = serializer.load(request.get_json())
            if user_id:
                token = create_access_token(identity=user_id)
                return jsonify({'status': True, 'msg': 'Login Sucessful', 'data': {'token': token}}), 200
            return jsonify({'status': False, 'msg': 'Email or password incorrect', 'data': None}), 404
        except ValidationError as err:
            return jsonify(
                {'status': False, 'msg': 'Validations failed', 'errors': err.messages, 'data': None}
            ), 400
