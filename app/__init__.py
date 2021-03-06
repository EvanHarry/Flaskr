from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/v1.0')

    from .task import task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/api/v1.0')

    return app
