import json


class Timeline:
    def __init__(self, json_filename):
        with open(json_filename, 'r') as json_file:
            json_data = json.load(json_file)
            self.actions = json_data['selfie']

    def get_actions(self):
        return self.actions
