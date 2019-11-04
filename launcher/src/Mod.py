from launcher.src import db
import json
import requests

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



    def postComputations(self, form):

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
        #appInfo = self.UserApps where id=appID
        #Example appInfo:
        appInfo = AppInfo(123, 'Awful App', 'Really awful application', 'noicon', dummySchema)
        appInfoDict = {}
        appInfoDict['id'] = appInfo.id
        appInfoDict['name'] = appInfo.name
        appInfoDict['description'] = appInfo.description
        appInfoDict['icon'] = appInfo.icon
        appInfoDict['schema'] = appInfo.schema

        ctName = formInfo['ctName']
        del formInfo['ctName']
        if ctName:
            pass
        else:
            return False

        if not self.ct_manager.validate(formInfo, appInfo.schema):
            return False

        ct = self.ct_manager.createCT(formInfo, appInfoDict, self.UserID, ctName)
        self.ct_manager.saveCT(ct)

        return ctName

        #return True


class CTManager:

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


    def createCT(self, formInfo, appInfoDict, UserID, ctName):
        
        ct = {}
        # ID taska będzie pewnie ustanawiany na podstawie stanu bazy tasków.
        ct['id'] = 1234
        ct['userId'] = UserID
        ct['name'] = ctName
        ct['application'] = appInfoDict
        ct['input'] = {}
        #ct['input']['logger'] = formInfo['logger']
        #del formInfo['logger']
        ct['input']['properties'] = formInfo

        return ct
        
    def saveCT(self, ct):
        def save_ct_to_database(computation_task):
            if CTStatistics.query.filter(CTStatistics.id == 1).count() < 1:
                stats = CTStatistics()
                stats.id = 1
                stats.next_value = 1
            else:
                stats = CTStatistics.query.filter(CTStatistics.id == 1).first()

            db_computation_task = ComputationTask()

            db_computation_task.id = stats.next_value
            stats.next_value = stats.next_value + 1
            stats.save()

            db_computation_task.user_id = computation_task['userId']
            db_computation_task.name = computation_task['name']
            db_computation_task.application = json.dumps(computation_task['application'])
            db_computation_task.input = json.dumps(computation_task['input'])
            db_computation_task.save()

        save_ct_to_database(ct)

        ctID = ct['id']
        userID = ct['userId']
        ctStorageName = str(userID) + str(ctID)
        with open(ctStorageName, 'w') as fp:
            json.dump(ct, fp)

    def getUserCT(self, userID):
        computation_tasks = ComputationTask.query.filter(ComputationTask.user_id == userID).all()
        return computation_tasks


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


class CTStatistics(db.Document):
    id = db.IntField()
    next_value = db.IntField()


class ComputationTask(db.Document):
    id = db.IntField()
    name = db.StringField()
    user_id = db.StringField()
    application = db.StringField()
    input = db.StringField()

    def __repr__(self):
        return f"User('{self.id}','{self.name}','{self.user_id}')"



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
