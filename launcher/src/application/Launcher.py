from requests import Timeout, ConnectTimeout
from launcher.src.application.Downloader import Downloader
from launcher.src.application.CTManager import CTManager
from launcher.src.model.Application import AppInfo
from launcher.src.model.ComputationTask import ComputationTask
import json
import requests
import re



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

        ct_to_post = computationTask.__repr__()

        try:
            resp = requests.post("http://localhost:5000/machine-manager/launcher/computations", json=json.dumps(ct_to_post))
            return resp
        except (ConnectionError, Timeout, ConnectionError, ConnectTimeout):
            return "I'm a teapot.", 418

        return False
