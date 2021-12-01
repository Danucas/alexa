from flask import Flask, jsonify, request
from api.v1.auth import auth_app
from api.v1.restaurants import restaurants_app
from rappi_api import Rappi
import os


app = Flask(__name__)


@app.route('/status/<user_device_id>')
def status(user_device_id):
    # Check for login status
    rappi_interface = Rappi(user_device_id)
    st = rappi_interface.get_account_status()
    return jsonify(status=st)


@app.route('/sign_status')
def sign_status():
    device_id = request.args.get('device_id')
    rappi_interface = Rappi(device_id)
    st = rappi_interface.login_status()
    print('Login status', st)
    return jsonify(status=st)



app.register_blueprint(auth_app, url_prefix='/api/v1/auth')
app.register_blueprint(restaurants_app, url_prefix='/api/v1/restaurants')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')
