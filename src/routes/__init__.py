from .user import user
from .organisation import org

url_prefix_blueprint = {
    '/api/user': user,
    '/api/organisation/': org,
}
