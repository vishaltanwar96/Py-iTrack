from flask import views, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from utils.misc_instances import db
from serializers.user import UserRegistrationSerializer, UserLoginSerializer


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
                db.session.rollback()
                return jsonify({'status': False, 'msg': err.messages}), 400
        return jsonify({'status': False, 'msg': 'Invalid JSON'}), 400


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
