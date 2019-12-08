from launcher.src.model.Application import AppInfo
import threading
import time
import requests
import json

class StatusGetter:
    Logs = []

    def thread_method(self):
        while True:
            try:
                #TODO: trzeba podać prawdziwą ścieżkę do logów
                logs = requests.get(url="http://127.0.0.1:7090/logs").json()
                self.Logs.append(logs)
            except Exception:
                pass
            time.sleep(5)


class Downloader:
    def __init__(self, AppDictionary = None):
        if AppDictionary is None:
            self.AppDictionary = {}
            self.Logs = []
            self.getStatus = StatusGetter()

    # Downloading Apps from path=/library/launcher/applications
    def downloadAppData(self, path):
        self.AppDictionary = requests.get(url=path).json()
        appInfos = []
        for app in self.AppDictionary:
            singleAppInfo = AppInfo(app['id'], app['name'],
                                    app['description'], app['icon'], json.loads(app['schema'].replace('\'','\"')))
            appInfos.append(singleAppInfo)


        return appInfos

    def run_thread(self):
        self.thread = threading.Thread(target=self.getStatus.thread_method)
        self.thread.start()

    def get_last_thread_data(self):
        return self.getStatus.Logs[self.getStatus.Logs.__len__()-1]

