from flask import Flask, send_from_directory, request, jsonify
from wml_utils import WMLHelper
from nlu_utils import NLUUtils
from get_vcap import get_wml_vcap, get_cos_vcap, get_vcap
import os

app = Flask(__name__, static_url_path='/static')

wml_vcap = get_wml_vcap()
nlu_vcap = get_vcap("nlu", None)

wml_client = WMLHelper(wml_vcap)
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


@app.route('/analyze', methods=['POST'])
def analyze():
    comment = request.get_json(force=True)
    print("Request to anayze: ")
    print(comment)
    try:
        response = wml_client.score_model(comment)
        return jsonify(response), 200
    except Exception as e:
        return str(e), 500

@app.route('/analyzesent', methods=['POST'])
def analyzesent():
    comment = request.get_data().decode('utf-8')
    sentiment = wml_client.analyze_sentiment(comment)
    # sentiment = nlu_utils.analyze_sentiment(comment)
    print("--> Comment: {}".format(comment))
    print("--> Sentiment: {}".format(sentiment))
    return sentiment

@app.route('/sentimentdeployments', methods=['GET'])
def areadeployments():
    deployment_array = wml_client.get_sentiment_functions()
    print("--> Sentiment deployments: {}".format(deployment_array))
    response = {
        "deployments" : deployment_array
    }
    return jsonify(response)

@app.route('/actionareadeployments', methods=['GET'])
def actiondeployments():
    deployment_array = wml_client.get_areaaction_functions()
    print("--> Action and area functions: {}".format(deployment_array))
    response = {
        "deployments" : deployment_array
    }
    return jsonify(response)

@app.route('/updatemodels', methods=['POST'])
def updatemodels():
    models = request.get_json(force=True)
    print("Request to anayze: ")
    print(models)
    try:
        wml_client.update_models(models)
        wml_client.update_scorings()
        return jsonify("ok"), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 500

@app.route('/checkdeployments', methods=['GET'])
def checkdeployments():
    if wml_client.check_deployments():
        return jsonify(True), 200
    else:
        return jsonify(False), 200

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=int(port))
