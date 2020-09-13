from flask import Blueprint

from controllers.organisation import OrganisationController

org = Blueprint('organisation', __name__)

org_view = OrganisationController.as_view('org_crud')
org.add_url_rule('/', view_func=org_view, methods=('GET', 'POST', 'PUT', 'DELETE'))
org.add_url_rule('/<int:org_id>/', view_func=org_view, methods=('GET', 'PUT', 'DELETE'))
