import json


class AppInfo:
    def __init__(self, id, name, description, icon, schema=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        if schema is None:
            self.schema = []
        else:
            self.schema = schema

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDesc(self):
        return self.description

    def getIcon(self):
        return self.icon

    def getSchema(self):
        return self.schema

    def __repr__(self):
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['description'] = self.description
        dict['icon'] = self.icon
        dict['schema'] = self.schema
        return json.dumps(dict)



class ComputationStep:
    def __init__(self, params, url, command):
        self.params = params
        self.artifactUrl = url
        self.command = command

    def __repr__(self):
        dict = {}
        dict['params'] = self.params
        dict['artifactUrl'] = self.artifactUrl
        dict['command'] = self.command
        return json.dumps(dict)


class ComputationStepParam:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self):
        dict = {}
        dict['name'] = self.name
        dict['type'] = self.type
        dict['defaultValue'] = self.value
        return json.dumps(dict)


class AppInfo:
    def __init__(self, id, name, description, icon, schema=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        if schema is None:
            self.schema = []
        else:
            self.schema = schema

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDesc(self):
        return self.description

    def getIcon(self):
        return self.icon

    def getSchema(self):
        return self.schema