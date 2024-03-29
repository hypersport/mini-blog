from flask import Flask
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import config
from flask_ckeditor import CKEditor

main = Blueprint('main', __name__)
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
ckeditor = CKEditor()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
login_manager.login_message = 'Log In First'

from . import myblog


def create_app(config_file):
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')
    app.config.from_object(config[config_file])
    db.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(main)
    return app
