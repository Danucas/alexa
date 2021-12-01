from flask import Flask, jsonify, request, send_file, abort, render_template
from api.v1.auth import auth_app
from api.v1.restaurants import restaurants_app
from rappi_api import Rappi
import os


app = Flask(__name__, template_folder=f'{os.getcwd()}/templates')


@app.route('/status/<user_device_id>')
def status(user_device_id):
    # Check for login status
    rappi_interface = Rappi(user_device_id)
    st = rappi_interface.get_account_status()
    return jsonify(status=st)


@app.route('/screenshot')
def screenshot():
    return send_file(f'{os.getcwd()}/screenshots/image.png', mimetype='image/png')


@app.route('/files', defaults={'req_path': ''})
@app.route('/files/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = f'{os.getcwd()}/screenshots'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)


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
