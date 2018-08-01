from watson_machine_learning_client import WatsonMachineLearningAPIClient
import random
import re
import uuid

class WMLHelper:
    def __init__(self, wml_vcap):
        print("Authentication ...")
        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())
        self.instance_id = wml_vcap["instance_id"]
        self.url = wml_vcap["url"]
        self.deployment_list = self.client.deployments.get_details()['resources']

        self.transaction_id = 'transaction-id-' + uuid.uuid4().hex
        print("--> Transaction ID:", self.transaction_id)

        self.area_action_deployment = ""
        self.sentiment_deployment = ""
        self.area_action_scoring_url = ""
        self.sentiment_scoring_url = ""
    
        self.get_sentiment_functions()
        self.get_areaaction_functions()
        self.update_scorings()

        self.neutral_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
                                  "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
                                  "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
                                  "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us."]

        self.negative_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly."]

        self.positive_templates = ["We are very happy to have provided you with such a positive experience!",
                                   "We are glad to hear you had such a great experience! ",
                                   "We appreciate your positive review about your recent experience with us!"]

    def score_model(self, request):
        print("--> Preparing for scoring.")
        gender = request['gender']
        status = request['status']
        comment = request['comment']
        childrens = int(request['childrens'])
        age = int(request['age'])
        customer_status = request['customer']
        car_owner = request['owner']
        satisfaction = request['satisfaction']

        fields = ['ID', 'Gender', 'Status', 'Children', 'Age',
                    'Customer_Status', 'Car_Owner', 'Customer_Service', 'Satisfaction']
        values = [11, gender, status, childrens, age,
                    customer_status, car_owner, comment, int(satisfaction)]

        print("--> Scoring Area/Action AI function.")
        print("--> Scoring url: {} ".format(self.area_action_scoring_url))
        payload_scoring = {"fields": fields, "values": [values]}
        print("--> Payload scoring:\n{}".format(payload_scoring))

        scoring = self.client.deployments.score(self.area_action_scoring_url, payload_scoring, transaction_id=self.transaction_id)
        print("--> Scoring result:\n{}".format(scoring))
        action_index = scoring['fields'].index('Prediction_Action')
        action_value = scoring['values'][0][action_index]

        area_index = scoring['fields'].index('Prediction_Area')
        area_value = scoring['values'][0][area_index]
        
        print("--> Area value: {}\n--> Action value: {}".format(area_value, action_value))

        client_response = ""
        if satisfaction == 0:
            client_response = self.negative_templates[random.randint(0, len(self.negative_templates)-1)].format(
                area_value.split(":")[0].lower(), area_value.split(":")[1].lower(), action_value.lower())
        elif satisfaction == 1:
            client_response = self.positive_templates[random.randint(
                0, len(self.positive_templates)-1)]
        else:
            print("--> Satisfaction field was not set properly.")

        return {"client_response": client_response, "action": action_value}

    def analyze_sentiment(self, text):
        print("--> Scoring Sentiment function.")

        payload = {
            'fields': ['feedback'],
            'values': [
                ["{}".format(text)]
            ]
        }

        print("--> Scoring payload:\n{}".format(payload))
        scoring = self.client.deployments.score(self.sentiment_scoring_url, payload, transaction_id=self.transaction_id)
        print("--> Scoring result:\n{}".format(scoring))

        sentiment_index = scoring['fields'].index('prediction_classes')
        sentiment_value = scoring['values'][0][sentiment_index][0]

        print("--> Predicted sentiment: {}".format(sentiment_value))
        return str(sentiment_value)

    def get_sentiment_functions(self):
        self.deployment_list = self.client.deployments.get_details()['resources']
        sentiment_array = []

        for deployment in self.deployment_list:
            deployment_name = deployment['entity']['name']
            if re.match(r'(.*)(sentiment|satisfaction)(.*)', deployment_name, re.IGNORECASE) and re.match(r'(.*)(function)(.*)', deployment_name, re.IGNORECASE):
                sentiment_array.append({
                    "name": deployment['entity']['name'],
                    "guid": deployment['metadata']['guid']
                })
        if len(sentiment_array) == 0:
            for deployment in self.deployment_list:
                sentiment_array.append({
                    "name": deployment['entity']['name'],
                    "guid": deployment['metadata']['guid']
                })

        if len(sentiment_array) > 0:
            self.sentiment_deployment = sentiment_array[0]['guid']
        
        print(sentiment_array)
        return sentiment_array

    def get_areaaction_functions(self):
        self.deployment_list = self.client.deployments.get_details()['resources']
        area_action_array = []

        for deployment in self.deployment_list:
            deployment_name = deployment['entity']['name']
            if re.match(r'(.*)(area)(.*)', deployment_name, re.IGNORECASE) and re.match(r'(.*)(function)(.*)', deployment_name, re.IGNORECASE):
                area_action_array.append({
                    "name": deployment['entity']['name'],
                    "guid": deployment['metadata']['guid']
                })
        if len(area_action_array) == 0:
            for deployment in self.deployment_list:
                area_action_array.append({
                    "name": deployment['entity']['name'],
                    "guid": deployment['metadata']['guid']
                })

        if len(area_action_array) > 0:
            self.area_action_deployment = area_action_array[0]['guid']
        
        return area_action_array

    def update_models(self, deployments):
        print("---> Update models:\n{}".format(deployments))
        self.area_action_deployment = deployments['areaaction']
        self.sentiment_deployment = deployments['sentiment']

    def update_scorings(self):
        print("--> Deployments:\nArea/Action: {}\nSentiment: {}".format(self.area_action_deployment, self.sentiment_deployment))
        
        for deployment in self.deployment_list:
            if self.area_action_deployment == deployment['metadata']['guid']:
                self.area_action_scoring_url = deployment['entity']['scoring_url']
            elif self.sentiment_deployment == deployment['metadata']['guid']:
                self.sentiment_scoring_url = deployment['entity']['scoring_url']

        print("--> Scoring urls:\nArea/Action: {}\nSentiment: {}".format(self.area_action_scoring_url, self.sentiment_scoring_url))

    def check_deployments(self):
        if len(self.area_action_scoring_url) == 0 or len(self.sentiment_scoring_url) == 0:
            return False
        return True
        