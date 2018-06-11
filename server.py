from flask import Flask, send_from_directory, request, jsonify
from wml_helper import WMLHelper
from nlu_utils import NLUUtils
from get_vcap import get_wml_vcap, get_cos_vcap, get_vcap
import os

app = Flask(__name__, static_url_path='/static')

wml_vcap = get_wml_vcap()
nlu_vcap = get_vcap("nlu", None)
cos_vcap = get_cos_vcap()

auth_endpoint = 'https://iam.bluemix.net/oidc/token' # only for us-south
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

wml_client = WMLHelper(wml_vcap, cos_vcap, auth_endpoint, service_endpoint)
nlu_utils = NLUUtils(nlu_vcap)


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

@app.route('/analyze', methods=['POST'])
def analyze():
    comment = request.get_json(force=True)
    return jsonify(wml_client.score_model(comment))

@app.route('/analyzesent', methods=['POST'])
def analyzesent():
    comment = request.get_data().decode('utf-8')
    sentiment = nlu_utils.analyze_sentiment(comment)
    print("--> Comment: {}".format(comment))
    print("--> Sentiment: {}".format(sentiment))
    return sentiment

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=int(port))
