from flask import Blueprint

from controllers.project import ProjectController

project = Blueprint('project', __name__)

project_view = ProjectController.as_view('project_crud')
project.add_url_rule('/', view_func=project_view, methods=('GET', 'POST'))
project.add_url_rule('/<int:project_id>/', view_func=project_view, methods=('GET', 'PUT', 'DELETE'))
