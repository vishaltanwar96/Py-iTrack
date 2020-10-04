from flask_smorest import Blueprint

project_bp = Blueprint(
    'project', __name__, url_prefix='/api/project', description='CRUD Views on Project Model'
)
