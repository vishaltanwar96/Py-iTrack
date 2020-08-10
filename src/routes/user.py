from flask import Blueprint

from controllers.user import UserController, UserLoginController


user = Blueprint('name', __name__)

user.add_url_rule('/', view_func=UserController.as_view('user_registration'))
user.add_url_rule('/login/', view_func=UserLoginController.as_view('user_login'))
