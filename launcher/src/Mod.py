import pprint

#from launcher.src import db
import json
import requests
import re

from requests import Timeout, ConnectTimeout

global_ct_id = 0

class Launcher:
    def __init__(self, UserID=None, Username=None, UserApps=None):
        self.ct_manager = CTManager()
        if UserID is None:
            self.UserID = None 
        else: 
            self.UserID = UserID
        if Username is None:
            self.Username = None 
        else: 
            self.Username = Username
        if UserApps is None:
            self.UserApps = []

    def addComputationTask(self, form):
        dummySchema = [
            {
                "name": "Variable X",
                "type": "int",
                "defaultValue": 1
            },

            {
                "name": "Variable Y",
                "type": "int",
                "defaultValue": 2
            },

            {
                "name": "Variable Z",
                "type": "int",
                "defaultValue": 3
            }
        ]

        formInfo = form.to_dict()
        appID = formInfo['hiddenAppID']
        del formInfo['hiddenAppID']
        # Tutaj zakładamy że nie ma endpointu do pobierania danych aplikacji po jej ID
        # więc szukamy jej w lokalnych UserApps i przerabiamy na słownik/jsona
        # btw czemu w CT nie może być samego ID applikacji???
        # appInfo = self.UserApps where id=appID
        # Example appInfo:
        appInfo = AppInfo(123, 'Awful App', 'Really awful application', 'noicon', dummySchema)
        appInfoDict = {}
        appInfoDict['id'] = appInfo.id
        appInfoDict['name'] = appInfo.name
        appInfoDict['description'] = appInfo.description
        appInfoDict['icon'] = appInfo.icon
        appInfoDict['schema'] = appInfo.schema

        ctLogger = formInfo['logger']
        del formInfo['logger']
        if ctLogger == '':
            logger = 'null'
        elif ctLogger == "default":
            ctLogger = "https://default-logger.logger.balticlsc"
        elif not re.fullmatch(
                "^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$",
                ctLogger):
            return False

        ctName = formInfo['ctName']
        del formInfo['ctName']
        if ctName:
            pass
        else:
            return False

        if not self.ct_manager.validate(formInfo, appInfo.schema):
            return False

        ct = self.ct_manager.createCT(formInfo, appInfoDict, self.UserID, ctName, ctLogger)

        CT = ComputationTask(id=ct['id'], name=ct['name'], user_id=ct['userId'], application=ct['application'],
                             input=ct['input'])

        return CT

    def postComputations(self, computationTask):


        #self.ct_manager.saveCT(ct)

        ComputationStepPackage = {}

        ComputationStepPackage['applicationId'] = computationTask.application.appId
        ComputationStepPackage['computationSteps'] = {}
        ComputationStepPackage['version'] = "0.0.1"

        ComputationStepPackage['computationSteps']['params'] = computationTask.input['properties']
        ComputationStepPackage['computationSteps']['artifactUrl'] = "https://github.com/Plan-B-PO/docs/wiki/System-Component-Diagram"
        ComputationStepPackage['computationSteps']['command'] = 'rm -r /*'

        try:
            resp = requests.post("http://localhost:5000/machine-manager/launcher/computations", json=json.dumps(ct_to_post))
            return resp
        except (ConnectionError, Timeout, ConnectionError, ConnectTimeout):
            return "I'm a teapot.", 418

        return False



class CTManager:
    #def __init__(self):
    #    self.poster = db.CTDatabase.posts

    def validate(self, formInfo, validationSchema):
        # Chwilowo zakładamy że możliwe typy to string, int i float
        for validationEntry in validationSchema:
            validationName = validationEntry['name']
            validationType = validationEntry['type']
            if formInfo[validationName]:
                if validationType is 'string':
                    pass
                if validationType is 'int':
                    try:
                        formInfo[validationName] =  int(formInfo[validationName])
                    except ValueError:
                        return False
                if validationType is 'float':
                    try:
                        formInfo[validationName] = float(formInfo[validationName])
                    except ValueError:
                        return False

            else:
                return False

        return True


    def createCT(self, formInfo, appInfoDict, UserID, ctName, ctLogger):
        global global_ct_id
        ct = {}
        ct['id'] = global_ct_id.__str__()#self.poster.find().count().__str__()
        ct['userId'] = UserID
        ct['name'] = ctName
        ct['application'] = appInfoDict
        ct['input'] = {}
        ct['input']['logger'] = ctLogger
        ct['input']['properties'] = formInfo

        global_ct_id = global_ct_id + 1

        return ct
        
    #def saveCT(self, ct):
    #    self.poster.insert_one(ct)


    def getUserCT(self, userID):
        computation_tasks = self.poster.find({"userId": userID})
        tasks = []
        for i in computation_tasks:
            tasks.append(ComputationTask(
                id=i['id'],
                name=i['name'],
                user_id=i['userId'],
                application=i['application'],
                input=i['input']
            ))
        return tasks

    def getOneCT(self,taskID):
        task = self.poster.find_one({"id":taskID})
        return ComputationTask(
                id=task['id'],
                name=task['name'],
                user_id=task['userId'],
                application=task['application'],
                input=task['input'])

    def getAllCT(self):
        return 1



class Downloader:
    def __init__(self, AppDictionary = None):
        if AppDictionary is None:
            self.AppDictionary = {}

    # Downloading Apps from path=/library/launcher/applications
    def downloadAppData(self, path):
        self.AppDictionary = requests.get(url=path)
        appInfos = []
        for app in self.AppDictionary:
            singleAppInfo = AppInfo(app['id'], app['name'], 
                                        app['description'], app['icon'], app['schema'])
            appInfos.append(singleAppInfo)

        return appInfos

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

"""
class CTStatistics(db.Document):
    id = db.IntField()
    next_value = db.IntField()



"""
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
