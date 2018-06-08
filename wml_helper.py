from watson_machine_learning_client import WatsonMachineLearningAPIClient
import random

class WMLHelper:
    def __init__(self, wml_vcap, cos_vcap, auth_endpoint, service_endpoint):
        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())
        self.cos_vcap = cos_vcap
        self.auth_endpoint = auth_endpoint
        self.service_endpoint = service_endpoint
        self.instance_id = wml_vcap["instance_id"]

        self.negative_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with {} {}. In the meantime, we’d like to offer you a coupon for a {} on your next rental with us.",
                                   "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with {} {}. In the meantime, we’d like to offer you a coupon for a {} on your next rental with us.",
                                   "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with {} {}. In the meantime, we’d like to offer you a coupon for a {} on your next rental with us.",
                                   "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with {} {}. In the meantime, we’d like to offer you a coupon for a {} on your next rental with us."]

        self.positive_templates = ["We are very happy to have provided you with such a positive experience!",
                                   "We are glad to hear you had such a great experience! ",
                                   "We appreciate your positive review about your recent experience with us!"]

    def score_model(self, request):
        scoring_url = "https://wml-fvt.stage1.machine-learning.ibm.com/v3/wml_instances/e63a814d-2e81-4e2f-a933-25582806958b/published_models/8b2c1349-33ca-4cc8-bb42-68b3ef817930/deployments/906bc7cb-9dc4-4733-9d60-011f4f082d3a/online"

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
                  customer_status, car_owner, comment, satisfaction]

        payload_scoring = {"fields": fields, "values": [values]}

        print("-> Scoring payload:\n{}".format(payload_scoring))

        scoring = self.client.deployments.score(scoring_url, payload_scoring)
        print("-> Scoring result:\n{}".format(scoring))

        area_index = scoring['fields'].index('predictedAreaLabel')
        action_index = scoring['fields'].index('predictedActionLabel')

        area_value = scoring['values'][0][area_index]
        action_value = scoring['values'][0][action_index]

        print("-> Area value: {}\nAction value: {}".format(area_value, action_value))

        client_response = ""
        if satisfaction == 0:
            client_response = self.negative_templates[random.randint(0, len(self.negative_templates)-1)].format(area_value.split(":")[0].lower(), area_value.split(":")[1].lower(), action_value.lower())
        else:
            client_response = self.positive_templates[random.randint(0, len(self.positive_templates)-1)]

        return {"client_response": client_response, "action": action_value}
