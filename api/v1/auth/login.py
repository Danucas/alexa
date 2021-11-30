from api.v1.auth import auth_app
from flask import jsonify, request
from rappi_api import Rappi
import json
import os
import time
import threading
from threading import Thread


def login_tread(device_id, action, phone):
    rappi_interface = Rappi(device_id)
    st = rappi_interface.login(action, phone)


@auth_app.route('/login', methods=['POST'])
def login():
    """
    Register a phone number in Rappi
    and return depending on the state a new request
    :return:
    """
    action = request.form.get('action')
    device_id = request.form.get('device_id')
    phone = request.form.get('phone')
    code = request.form.get('code')

    if not action:
        return jsonify(error='Missing field <action>'), 403
    if not phone:
        return jsonify(error='Missing field <phone>'), 403
    if (action == 'sms' or action == 'email') and not code:
        return jsonify(error='Missing field <code>'), 403

    if action == 'init':
        status_path = f'{os.getcwd()}/sessions/{device_id}.status'
        try:
            os.remove(status_path)
        except:
            pass
        Thread(target=login_tread, args=(device_id, action, phone)).start()
        # while not check_login_status(device_id):
        #     time.sleep(1)
        # time.sleep(1)
        return jsonify(next_action='sms')

    elif action == 'sms' or action == 'email':
        save_status(device_id, action, code)
        while get_status(device_id)['action'] == action:
            time.sleep(1)
        time.sleep(1)
        return jsonify(next_action=get_status(device_id)['action'])


def save_status(device_id, st, code):
    status_path = f'{os.getcwd()}/sessions/{device_id}.status'
    with open(status_path, 'w') as status_file:
        status_file.write(json.dumps({
            "action": st,
            "code": code
        }))

def get_status(device_id):
    status_path = f'{os.getcwd()}/sessions/{device_id}.status'
    with open(status_path, 'r') as status_file:
        return json.loads(status_file.read())


def check_login_status(device_id):
    status_path = f'{os.getcwd()}/sessions/{device_id}.status'
    if os.path.exists(status_path):
        return True
    else:
        return False
