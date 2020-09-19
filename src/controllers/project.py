from flask import views, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_current_user

from utils import db
from utils.helpers import super_users_only
from models import Status, user_organisation_table, Project
from serializers.project import CreateProjectSerializer


class ProjectController(views.MethodView):
    """Project CRUD Views"""

    @super_users_only
    def post(self):
        """Create a project"""

        if request.is_json:

            current_user = get_current_user()
            if not current_user:
                return jsonify({'status': False, 'msg': 'User doesn\'t exist', 'data': None}), 404

            current_user_id = current_user.id

            try:
                request_data = request.get_json()

                if Project.query.filter_by(name=request_data['name']).first():
                    return jsonify({'status': False, 'msg': 'Project already exists', 'data': None}), 400

                serializer = CreateProjectSerializer()

                validated_data = serializer.load(request_data)

                validated_data['created_by'] = current_user_id

                status = Status.query.filter_by(value='WIP').first()
                if not status:
                    return jsonify(
                        {'status': False, 'msg': 'Invalid status, doesn\'t exist', 'data': None}
                    ), 404

                validated_data['status_id'] = status.id

                organisation = db.session.query(user_organisation_table). \
                    filter(user_organisation_table.c.user_id == current_user_id).first()

                if not organisation:
                    return jsonify(
                        {'status': False, 'msg': 'User not associated with any organisation', 'data': None}
                    ), 404

                validated_data['organisation_id'] = organisation.organisation_id
                project = Project(**validated_data)
                db.session.add(project)
                db.session.commit()
                return jsonify(
                    {'status': True, 'msg': 'Project created successully', 'data': {'id': project.id}}
                ), 201
            except ValidationError as err:
                return jsonify({'status': False, 'msg': 'Validation failed', 'data': None, 'errors': err.messages}), 400

        return jsonify({'status': False, 'msg': 'Invalid JSON', 'data': None}), 400

    @jwt_required
    def get(self, project_id=None):
        """Get all projects or project using id"""
        pass

    @super_users_only
    def put(self, project_id=None):
        """Change project details using id"""
        pass

    @super_users_only
    def delete(self, project_id=None):
        """Delete a project using id"""
        pass
