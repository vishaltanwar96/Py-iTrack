from flask import Blueprint

from controllers.user import UserController, UserLoginController


user = Blueprint('name', __name__)

user_view = UserController.as_view('user_crud')
user.add_url_rule('/', view_func=user_view, methods=('GET', 'POST'))
user.add_url_rule('/<int:user_id>/', view_func=user_view, methods=('GET', 'POST'))
user.add_url_rule('/login/', view_func=UserLoginController.as_view('user_login'))
