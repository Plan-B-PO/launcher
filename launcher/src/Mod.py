import pprint

#from launcher.src import db
import json
import requests
import re

from requests import Timeout, ConnectTimeout

global_ct_id = 0











"""
class CTStatistics(db.Document):
    id = db.IntField()
    next_value = db.IntField()



"""


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



