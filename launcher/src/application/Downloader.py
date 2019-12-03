from launcher.src.model.Application import AppInfo
import requests


class Downloader:
    def __init__(self, AppDictionary = None):
        if AppDictionary is None:
            self.AppDictionary = {}

    # Downloading Apps from path=/library/launcher/applications
    def downloadAppData(self, path):
        self.AppDictionary = requests.get(url=path)
        appInfos = []
        print(self.AppDictionary)
        for app in self.AppDictionary:
            singleAppInfo = AppInfo(app['id'], app['name'],
                                    app['description'], app['icon'], app['schema'])
            appInfos.append(singleAppInfo)


        return appInfos
