import json

from flask_login import LoginManager, UserMixin
from webapp.auth import User
from flask import Flask

def read_configuration(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config["flask_secret_key"]


def create_app():
    app = Flask(__name__)
    flask_key = read_configuration("webapp\mddns-gui-config.json")
    app.config['SECRET_KEY'] = flask_key

    from .views import views
    from .auth import auth
    from .dashboard import dashboard

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    return app
