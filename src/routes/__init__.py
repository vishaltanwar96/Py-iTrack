from .user import user
from .organisation import org
from .project import project

url_prefix_blueprint = {
    '/api/user': user,
    '/api/organisation': org,
    '/api/project': project,
}
