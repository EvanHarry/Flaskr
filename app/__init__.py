from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.index'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/v1.0')

    from .task import task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/api/v1.0')

    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
