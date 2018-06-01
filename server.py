from flask import Flask, send_from_directory, request
from wml_helper import WMLHelper
from get_vcap import get_wml_vcap, get_cos_vcap

app = Flask(__name__, static_url_path='/static')

wml_vcap = get_wml_vcap()
cos_vcap = get_cos_vcap()

auth_endpoint = 'https://iam.bluemix.net/oidc/token' # only for us-south
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

wml_client = WMLHelper(wml_vcap, cos_vcap, auth_endpoint, service_endpoint)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/stylesheets/<path:path>')
def send_styles(path):
    return send_from_directory('static/stylesheets', path)


@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('static/scripts', path)


@app.route('/staticImages/<path:path>')
def send_img(path):
    return send_from_directory('static/images', path)


@app.route('/comments', methods=['POST'])
def process_comment():
    comment = request.get_data().decode('utf-8')

    # TODO do some model magic

    return 'Oh dear... We don\'t know what to say to \'' + comment + '\'!'
