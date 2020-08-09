from flask import Blueprint

from controllers.user import UserController


user = Blueprint('name', __name__)

user.add_url_rule('/', view_func=UserController.as_view('user_registration'))
