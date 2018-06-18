from watson_machine_learning_client import WatsonMachineLearningAPIClient
import random

class WMLHelper:
    def __init__(self, wml_vcap, cos_vcap, auth_endpoint, service_endpoint):
        print("Authentication ...")
        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())
        self.cos_vcap = cos_vcap
        self.auth_endpoint = auth_endpoint
        self.service_endpoint = service_endpoint
        self.instance_id = wml_vcap["instance_id"]
        print("Authentication finished.")

        # self.negative_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
        #                            "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
        #                            "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
        #                            "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us."]
        
        self.negative_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly."]

        self.positive_templates = ["We are very happy to have provided you with such a positive experience!",
                                   "We are glad to hear you had such a great experience! ",
                                   "We appreciate your positive review about your recent experience with us!"]

    def score_model(self, request):
        # scoring_url = "https://wml-fvt.stage1.machine-learning.ibm.com/v3/wml_instances/e63a814d-2e81-4e2f-a933-25582806958b/published_models/8b2c1349-33ca-4cc8-bb42-68b3ef817930/deployments/906bc7cb-9dc4-4733-9d60-011f4f082d3a/online"
        # scoring_url = "https://wml-fvt.stage1.machine-learning.ibm.com/v3/wml_instances/b1875b6a-9af3-4f77-9002-da52ca0a9610/published_models/d2154fbc-03ef-4920-85ce-6c6c9e40c547/deployments/6c4a0c31-5ecc-49d2-aa8e-2535af3271f4/online"
        #scoring_url = "https://wml-fvt.stage1.machine-learning.ibm.com/v3/wml_instances/b1875b6a-9af3-4f77-9002-da52ca0a9610/published_models/1cb8ff33-93fe-4666-b99a-85ee3eb8d387/deployments/85eb51b6-b09d-45bb-bd0b-60968ea250c6/online"
        scoring_url = "https://wml-fvt.stage1.machine-learning.ibm.com/v3/wml_instances/b1875b6a-9af3-4f77-9002-da52ca0a9610/published_models/98b137ec-b5c3-4f2a-8f5c-d32af126e439/deployments/7f0b3eb0-88f0-4220-b8ec-2d0ec8357cff/online"

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
