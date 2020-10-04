from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
api = Api()
