from flask_smorest import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/api/user', description='User Related Views')
