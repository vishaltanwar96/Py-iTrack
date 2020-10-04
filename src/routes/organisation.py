from flask_smorest import Blueprint

org_bp = Blueprint(
    'organisation', __name__, url_prefix='/api/organisation', description='CRUD Views on Organisation Model'
)
