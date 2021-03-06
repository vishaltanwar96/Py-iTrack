import os
from configparser import ConfigParser

from flask import Flask
from flask_cors import CORS

from routes import url_prefix_blueprint
from commands import blueprint_cli_group_mapping
from utils.misc_instances import db, ma, migrate, jwt


class Application(object):
    """Application Factory Class"""

    INSTANCE = None
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ENV_FILE: str = os.environ.get('ENV', 'development')

    def __init__(self, name: str) -> None:
        """."""

        config = ConfigParser()
        config.read(os.path.join(self.BASE_DIR, 'resources', f'{self.ENV_FILE.lower()}.ini'))

        self.app: Flask = Flask(name)
        self.app.config.update(
            BASE_DIR=self.BASE_DIR,
            HOST='0.0.0.0',
            PORT=config.getint('DEFAULT', 'PORT'),
            DEBUG=config.getboolean('DEFAULT', 'DEBUG'),
            ENV=config.get('DEFAULT', 'ENV'),
            SQLALCHEMY_DATABASE_URI=config.get('DEFAULT', 'SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=config.getboolean('DEFAULT', 'SQLALCHEMY_TRACK_MODIFICATIONS'),
            SECRET_KEY=config.get('DEFAULT', 'SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES=config.getint('DEFAULT', 'JWT_ACCESS_TOKEN_EXPIRES')
        )
        db.init_app(self.app)
        ma.init_app(self.app)
        migrate.init_app(self.app, db)
        jwt.init_app(self.app)

        CORS(self.app)
        self.register_blueprints(url_prefix_blueprint)
        self.register_blueprints(blueprint_cli_group_mapping)

    def register_blueprints(self, blueprint_prefix_dict: dict) -> None:
        for url_prefix, blueprint in blueprint_prefix_dict.items():
            self.app.register_blueprint(blueprint, url_prefix=url_prefix)

    @classmethod
    def get_instance(cls, name: str) -> Flask:
        """."""

        if not cls.INSTANCE:
            cls.INSTANCE: Application = Application(name)

        return cls.INSTANCE.app
