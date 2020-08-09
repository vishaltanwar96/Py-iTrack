from flask import views, request, jsonify
from marshmallow import ValidationError

from utils import db
from serializers.user import UserRegistrationSerializer


class UserController(views.MethodView):
    """User CRUD Views"""

    def post(self, *args, **kwargs):
        """Creates a User (User Registration)"""

        if request.is_json:
            serializer = UserRegistrationSerializer()
            try:
                user = serializer.load(**request.get_json())
                db.session.add(user)
                db.session.commit()
                return jsonify({'status': True, 'msg': 'Registration Successful'}), 200
            except ValidationError as err:
                db.session.rollback()
                return jsonify({'status': False, 'msg': err.messages}), 400
        return jsonify({'status': False, 'msg': 'Invalid JSON'}), 400
