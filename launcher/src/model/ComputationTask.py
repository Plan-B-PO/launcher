import json


class ComputationTask:
    id = ''
    name = ''
    user_id = ''

    def __init__(self, id, name, user_id, application, input):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.application = application
        self.input = input

    def __repr__(self):
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['userId'] = self.user_id
        dict['application'] = self.application
        dict['input'] = self.input
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