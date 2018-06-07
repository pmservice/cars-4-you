from watson_machine_learning_client import WatsonMachineLearningAPIClient

class WMLHelper:
    def __init__(self, wml_vcap, cos_vcap, auth_endpoint, service_endpoint):
        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())
        self.cos_vcap = cos_vcap
        self.auth_endpoint = auth_endpoint
        self.service_endpoint = service_endpoint
        self.instance_id = wml_vcap["instance_id"]


    def score_model(self, request):
        scoring_url = "https://wml-fvt.stage1.machine-learning.ibm.com/v3/wml_instances/e63a814d-2e81-4e2f-a933-25582806958b/published_models/8b2c1349-33ca-4cc8-bb42-68b3ef817930/deployments/906bc7cb-9dc4-4733-9d60-011f4f082d3a/online"

        gender = request['gender']
        status = request['status']
        comment = request['comment']
        childrens = int(request['childrens'])
        age = int(request['age'])
        customer_status = request['customer']
        car_owner = request['owner']

        fields = ['ID', 'Gender', 'Status', 'Children', 'Age', 'Customer_Status','Car_Owner', 'Customer_Service', 'Satisfaction']
        values = [11, gender, status, childrens, age, customer_status, car_owner, comment, 0]

        payload_scoring = {"fields": fields,"values": [values]}

        print("-> Scoring payload:\n{}".format(payload_scoring))

        scoring = self.client.deployments.score(scoring_url, payload_scoring)
        print("-> Scoring result:\n{}".format(scoring))

        area_index = scoring['fields'].index('predictedAreaLabel')
        action_index = scoring['fields'].index('predictedActionLabel')

        area_value = scoring['values'][0][area_index]
        action_value = scoring['values'][0][action_index]

        print("-> Area value: {}\nAction value: {}".format(area_value, action_value))

        return {"area": area_value, "action": action_value}
