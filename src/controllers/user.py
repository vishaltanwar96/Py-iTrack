from flask import views, request, jsonify
from sqlalchemy import update
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from models.user import User
from utils.misc_instances import db
from serializers.user import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserChangeDetailsSerializer,
)


class UserController(views.MethodView):
    """User CRUD Views"""

    def post(self, *args, **kwargs):
        """Creates a User (User Registration)"""

        if request.is_json:
            serializer = UserRegistrationSerializer()
            try:
                user = serializer.load(request.get_json())
                db.session.add(user)
                db.session.commit()
                return jsonify({'status': True, 'msg': 'Registration Successful'}), 201
            except ValidationError as err:
                return jsonify({'status': False, 'msg': 'Field validations failed', 'errors': err.messages}), 400
        return jsonify({'status': False, 'msg': 'Invalid JSON'}), 400

    def get(self, user_id=None, *args, **kwargs):
        """Get a User or a List of Users"""

        if not user_id:
            users = User.query.all()
            serializer = UserSerializer(many=True)
            return jsonify({'status': False, 'msg': 'Fetched data successfully', 'data': serializer.dump(users)}), 200
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'status': False, 'msg': 'User doesn\'t exist'}), 404
        serializer = UserSerializer()
        return jsonify({'status': False, 'msg': 'Fetched data successfully', 'data': serializer.dump(user)}), 200

    def put(self, user_id, *args, **kwargs):
        """Change User Information"""

        if not user_id:
            return jsonify({'status': False, 'msg': 'No user id specified'}), 400
        user = User.query.filter_by(id=user_id)
        if not user:
            return jsonify({'status': False, 'msg': 'User doesn\'t exist'}), 404
        if request.is_json:
            serializer = UserChangeDetailsSerializer()
            try:
                update_data = serializer.load(request.get_json())
                user.update(update_data)
                db.session.commit()
                return jsonify({'status': True, 'msg': 'Details saved successfully'}), 200
            except ValidationError as err:
                return jsonify({'status': False, 'msg': 'Field validations Failed', 'errors': err.messages}), 400


class UserLoginController(views.MethodView):
    """User Login"""

    def post(self, *args, **kwargs):
        """Handle User Login"""

        if request.is_json:
            serializer = UserLoginSerializer()
            try:
                user_id = serializer.load(request.get_json())
                if user_id:
                    token = create_access_token(identity=user_id)
                    return jsonify({'status': True, 'msg': 'Login Sucessful', 'token': token}), 200
                return jsonify({'status': False, 'msg': 'Email or password incorrect', 'token': None}), 404
            except ValidationError as err:
                return jsonify({'status': False, 'msg': err.messages}), 400
        return jsonify({'status': False, 'msg': 'Invalid JSON'}), 400
