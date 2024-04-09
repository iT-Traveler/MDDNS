from flask import Blueprint, render_template, flash, redirect, url_for
from flask import Flask, render_template, request, jsonify
import requests
import json
from flask_login import login_required, current_user
from webapp import dbcalls


dashboard = Blueprint('dashboard', __name__)

API_BASE_URL = 'https://mddns.azurewebsites.net'

def make_api_call(endpoint, method='GET', data=None):
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {'Content-Type': 'application/json', 'X-API-Key': f'{your_api_key}'}
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, data=json.dumps(data), headers=headers)
    elif method == 'PUT':
        response = requests.put(url, data=json.dumps(data), headers=headers)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    return response.json()

@dashboard.route('/dashboard')
@login_required
def dashboard_view():
    global your_api_key
    user_id = current_user.id
    your_api_key = dbcalls.read_api_key_by_oauthkey(user_id)
    return render_template("dashboard.html",user=current_user, user_id=user_id)

@dashboard.route('/create', methods=['POST'])
def handle_create():
    data = request.form
    payload = {'subdomain': data['field1'], 'ip': data['field2']}
    flash(make_api_call('subdomain/new', 'POST', payload))
    return redirect(url_for('dashboard.dashboard_view'))

# Route for updating an existing subdomain
@dashboard.route('/update', methods=['POST'])
def handle_update():
    data = request.form
    payload = {'ip': data['field2']}
    flash(make_api_call(f"subdomain/name/{data['field1']}", 'PUT', payload))
    return redirect(url_for('dashboard.dashboard_view'))

# Route for deleting an existing subdomain
@dashboard.route('/delete', methods=['POST'])
def handle_delete():
    data = request.form
    flash(make_api_call(f"subdomain/name/{data['field']}", 'DELETE'))
    return redirect(url_for('dashboard.dashboard_view'))

# Route for reading an existing subdomain information
@dashboard.route('/read', methods=['POST'])
def handle_read():
    data = request.form
    flash(make_api_call(f"subdomain/name/{data['field']}", 'GET'))
    return redirect(url_for('dashboard.dashboard_view'))