from watson_machine_learning_client import WatsonMachineLearningAPIClient
import random


class WMLHelper:
    def __init__(self, wml_vcap):
        print("Authentication ...")
        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())
        self.instance_id = wml_vcap["instance_id"]
        self.url = wml_vcap["url"]
        self.deployment_list = self.client.deployments.get_details()['resources']
    
        self.area_deployment = ""
        self.action_deployment = ""        
        self.area_scoring_url = ""
        self.action_scoring_url = ""
        
        self.get_action_deployments()
        self.get_area_deployments()
        self.update_scorings()
        
        print("Authentication finished.")

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

        scoring = self.client.deployments.score(self.area_scoring_url, payload_scoring)
        print("-> Scoring result:\n{}".format(scoring))
        area_index = scoring['fields'].index('predictedLabel')
        area_value = scoring['values'][0][area_index]

        scoring = self.client.deployments.score(self.action_scoring_url, payload_scoring)
        print("-> Scoring result:\n{}".format(scoring))        
        action_index = scoring['fields'].index('predictedLabel')
        action_value = scoring['values'][0][action_index]

        print("-> Area value: {}\nAction value: {}".format(area_value, action_value))

        client_response = ""
        if satisfaction == 0:
            client_response = self.negative_templates[random.randint(0, len(self.negative_templates)-1)].format(
                area_value.split(":")[0].lower(), area_value.split(":")[1].lower(), action_value.lower())
        else:
            client_response = self.positive_templates[random.randint(
                0, len(self.positive_templates)-1)]

        return {"client_response": client_response, "action": action_value}

    def get_area_deployments(self):
        deployment_array = []

        for deployment in self.deployment_list:
            if "area" in deployment['entity']['name'].lower():
                deployment_array.append(deployment['entity']['name'])
        if len(deployment_array) == 0:
            for deployment in self.deployment_list:
                deployment_array.append(deployment['entity']['name'])

        if len(deployment_array) > 0:
            self.area_deployment = deployment_array[0]
            
        return deployment_array

    def get_action_deployments(self):
        deployment_array = []

        print(self.deployment_list)
        for deployment in self.deployment_list:
            if "action" in deployment['entity']['name'].lower():
                deployment_array.append(deployment['entity']['name'])
        if len(deployment_array) == 0:
            for deployment in self.deployment_list:
                deployment_array.append(deployment['entity']['name'])
        
        if len(deployment_array) > 0:
            self.action_deployment = deployment_array[0]
            
        return deployment_array


    def update_models(self, deployments):
        self.area_deployment = deployments['area']
        self.action_deployment = deployments['action']

    def update_scorings(self):
        print("--> Deployments urls:\narea: {}\naction: {}".format(self.action_deployment, self.area_deployment))
        for deployment in self.deployment_list:
            if self.area_deployment == deployment['entity']['name']:
                self.area_scoring_url = deployment['entity']['scoring_url']
            elif self.action_deployment == deployment['entity']['name']:
                self.action_scoring_url = deployment['entity']['scoring_url']

        print("--> Scoring urls:\narea: {}\naction: {}".format(self.area_scoring_url, self.action_scoring_url))

    def check_deployments(self):
        if len(self.area_scoring_url) == 0 or len(self.action_scoring_url) == 0:
            return False
        return True
        