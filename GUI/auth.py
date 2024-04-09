import json

from flask import Flask, render_template, request, make_response, Blueprint
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
from webapp.config import CONFIG
from flask import Flask, redirect, url_for
from flask_login import login_user, login_required, logout_user, UserMixin
from webapp import dbcalls

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

def read_configuration(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config["flask_secret_key"]

auth = Blueprint('auth', __name__)
flask_key = read_configuration("webapp\mddns-gui-config.json")
authomatic = Authomatic(CONFIG, flask_key, report_errors=False)


@auth.route('/login/<provider_name>/')
def login(provider_name):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    if result:
        if result.user:
            result.user.update()

            email = result.user.email
            user_id = result.user.id
            user = User(user_id)
            login_user(user)

            dbcalls.check_user_exists_by_oauthkey(user_id, email)
            return redirect(url_for('dashboard.dashboard_view'))

    return response

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
