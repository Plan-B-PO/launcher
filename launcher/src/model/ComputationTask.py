import json

default_csp = {
        "applicationId": "",
        "computationSteps":[
            {
                "artifactUrl": "fib_list:latest",
                "command": "",
                "params": [
                    {
                        "name": "N",
                        "type": "int",
                        "defaultValue": 10
                    }
                ]
            },
            {
                "params": [],
                "artifactUrl": "fib_sum:latest",
                "command": ""
            }
        ],
        "version":"0.01.1"
    }


class ComputationTask:
    id = ''
    name = ''
    user_id = ''
    logs = []
    status='unknown'
    computation_step_package = {
    }

    def __init__(self, id, name, user_id, application, input, mm_ct_id, computation_step_package=default_csp):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.application = application
        self.input = input
        self.mm_ct_id = mm_ct_id
        self.computation_step_package = computation_step_package
        self.computation_step_package["applicationId"] = application['id']

        for i in range(10):
            self.logs.append("Log " + i.__str__())

    def __repr__(self):
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['userId'] = self.user_id
        dict['application'] = self.application
        dict['input'] = self.input
        dict['computationStepPackage'] = self.computation_step_package
        return dict

    def __str__(self):
        dict = self.__repr__()
        return json.dumps(dict)

class InputDataEntry:
    def __init__(self,name,value):
        self.name = name
        self.value = value


class FormEntry:
    def __init__(self, name, type, defaultValue):
        if name is None:
            self.name = None
        else:
            self.name = name
        if type is None:
            self.type = None
        else:
            self.type = type
        if defaultValue is None:
            self.defaultValue = None
        else:
            self.defaultValue = defaultValue