from marshmallow import ValidationError
from flask import views, jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils import db
from utils.helpers import get_super_users
from models import Organisation, User, user_organisation_table
from serializers.organisation import (
    OrganisationSerializer,
    OrganisationRegistrationSerializer
)


class OrganisationController(views.MethodView):
    """Organisation CRUD Views"""

    decorators = (jwt_required,)

    def get(self, org_id=None, *args, **kwargs):
        """Gets all organisations or organisation details based on org_id"""

        if not org_id:
            serializer = OrganisationSerializer(many=True)
            return jsonify(
                {'status': True, 'msg': 'Data fetched sucessfully', 'data': serializer.dump(Organisation.query.all())}
            ), 200

        organisation = Organisation.query.get(org_id)

        if not organisation:
            return jsonify({'status': False, 'msg': 'Organisation doesn\'t exist', 'data': None}), 404

        return jsonify(
            {'status': True, 'msg': 'Data fetched sucessfully', 'data': OrganisationSerializer().dump(organisation)}
        ), 200

    def post(self, *args, **kwargs):
        """Register an orgsanition"""

        if request.is_json:
            current_user_id = get_jwt_identity()

            current_user = User.query.get(current_user_id)

            if not current_user:
                return jsonify({'status': False, 'msg': 'User doesn\'t exist', 'data': None}), 404

            if current_user.role_id not in get_super_users():
                return jsonify({'status': False, 'msg': 'Action not permissible', 'data': None}), 403

            if db.session.query(user_organisation_table).\
                    filter(user_organisation_table.c.user_id == current_user_id).first():
                return jsonify(
                    {'status': False, 'msg': 'A user can be associated with only one organisation', 'data': None}
                ), 400

            request_data = request.get_json()

            if Organisation.query.filter_by(name=request_data.get('name')).first():
                return jsonify({'status': False, 'msg': 'Organisation already exists', 'data': None}), 400

            serializer = OrganisationRegistrationSerializer()

            try:
                validated_request_data = serializer.load(request_data)
                validated_request_data['passcode'] = generate_password_hash(
                    password=validated_request_data.pop('passcode')
                )
                validated_request_data['registered_by'] = current_user_id
                organisation = Organisation(**validated_request_data)
                organisation.user_organisation.append(current_user)
                db.session.add(organisation)
                db.session.commit()
                return jsonify(
                    {'status': True, 'msg': 'Organisation registation successful', 'data': {'id': organisation.id}}
                ), 201
            except ValidationError as err:
                return jsonify({'status': False, 'msg': 'Validation failed', 'data': None, 'errors': err.messages}), 400
        return jsonify({'status': False, 'msg': 'Invalid JSON', 'data': None}), 400
