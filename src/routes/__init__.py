from .user import user_bp
from .organisation import org_bp
from .project import project_bp

api_blueprints = [
    user_bp,
    org_bp,
    project_bp,
]
