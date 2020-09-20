from flask import views, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity

from utils import db
from utils.helpers import super_users_only, verify_json_request
from models import Status, user_organisation_table, Project, Role, User
from serializers.project import (
    CreateProjectSerializer,
    ProjectSerializer,
)


class ProjectController(views.MethodView):
    """Project CRUD Views"""

    @super_users_only
    @verify_json_request
    def post(self):
        """Create a project"""

        current_user = get_current_user()
        if not current_user:
            return jsonify({'status': False, 'msg': 'User doesn\'t exist', 'data': None}), 404

        current_user_id = current_user.id

        try:
            request_data = request.get_json()

            serializer = CreateProjectSerializer()

            validated_data = serializer.load(request_data)

            if Project.query.filter_by(name=request_data.get('name')).first():
                return jsonify({'status': False, 'msg': 'Project already exists', 'data': None}), 400

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
            project.project_users.append(current_user)
            db.session.add(project)
            db.session.commit()
            return jsonify(
                {'status': True, 'msg': 'Project created successully', 'data': {'id': project.id}}
            ), 201
        except ValidationError as err:
            return jsonify({'status': False, 'msg': 'Validation failed', 'data': None, 'errors': err.messages}), 400

    @jwt_required
    def get(self, project_id=None):
        """Get all projects or project using id"""

        if not project_id:
            serializer = ProjectSerializer(many=True)
            role_project_to_show_map = {
                Role.query.filter_by(value='ADMIN').first().id: Project.query.all(),
                Role.query.filter_by(value='MANAGER').first().id: Project.query.filter_by(
                    organisation_id=db.session.query(user_organisation_table).filter(
                        user_organisation_table.c.user_id == get_jwt_identity()).first().organisation_id
                ).all(),
                Role.query.filter_by(value='RESOURCE').first().id: User.query.get(get_jwt_identity()).user_projects,
            }
            return jsonify(
                {
                    'status': True,
                    'msg': 'Data fetched successfully',
                    'data': serializer.dump(role_project_to_show_map[get_current_user().role_id])
                }
            ), 200
        serializer = ProjectSerializer()
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'status': False, 'msg': 'Invalid Project ID, not found', 'data': None}), 404
        return jsonify({'status': True, 'msg': 'Data fetched successfully', 'data': serializer.dump(project)}), 200

    @super_users_only
    @verify_json_request
    def put(self, project_id=None):
        """Change project details using id"""
        pass

    @super_users_only
    def delete(self, project_id=None):
        """Delete a project using id"""
        pass
