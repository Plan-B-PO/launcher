from launcher.src.model.Application import AppInfo
import requests
import json


class Downloader:
    def __init__(self, AppDictionary = None):
        if AppDictionary is None:
            self.AppDictionary = {}

    # Downloading Apps from path=/library/launcher/applications
    def downloadAppData(self, path):
        self.AppDictionary = requests.get(url=path).json()
        appInfos = []
        for app in self.AppDictionary:
            singleAppInfo = AppInfo(app['id'], app['name'],
                                    app['description'], app['icon'], json.loads(app['schema'].replace('\'','\"')))
            appInfos.append(singleAppInfo)


        return appInfos
