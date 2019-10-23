from flask import Flask
from flask import request
import json
import requests

class Launcher:
    def __init__(self, UserID=None, Username=None, UserApps=None):
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
        ctm = CTManager()
        formInfo = form.to_dict(flat=False)
        """ if not ctm.validate(response):
            print('Invlid input') """

        ct = ctm.createCT(formInfo, appInfo, self.UserID)
        ctm.saveCT(ct)


class CTManager:
    def validate(self):
        return
    def createCT(self, formInfo, appInfo, UserID):
        
    
        ct = {}
        ct['id'] = 1234
        ct['userID'] = UserID
        ct['name'] = formInfo['name']
        del formInfo['name']
        ct['application'] = appInfo
        ct['input'] = {}
        ct['input']['logger'] = formInfo['logger']
        del formInfo['logger']
        ct['input']['properties'] = formInfo

        
        return ct

        
    def saveCT(self, ct):
        ctID = ct['id']
        userID = ct['userID']
        ctStorageName = str(userID) + str(ctID)
        with open(ctStorageName, 'w') as fp:
            json.dump(ct, fp)


class Downloader:
    def __init__(self, AppDictionary = None):
        if AppDictionary is None:
            self.AppDictionary = {}

    # Downloading Apps from path=/library/launcher/applications
    def downloadAppData(self, path):
        self.AppDictionary = requests.get(url=path)
        appInfos = []
        for app in range(len(self.AppDictionary)):
            singleAppInfo = AppInfo(self.AppDictionary[app]['id'], self.AppDictionary[app]['name'], 
                                        self.AppDictionary[app]['description'], self.AppDictionary[app]['icon'])
            appInfos.append(singleAppInfo)

        return appInfos

class AppInfo:
    def __init__(self, id, name, description, icon):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon

    def getId(self):
        return self.id
    
    def getName(self):
        return self.name

    def getDesc(self):
        return self.description

    def getIcon(self):
        return self.icon