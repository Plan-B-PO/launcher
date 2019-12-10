from launcher.src.model.Application import AppInfo
import threading
import time
import requests
import json
import queue

class StatusGetter:
    logs = {}#TODO: słownik
    queue = queue.Queue(1024)

    def thread_method(self):
        while True:
            try:
                id = self.queue.get(False)
                #TODO: trzeba podać prawdziwą ścieżkę do logów
                logs = requests.get(url="http://127.0.0.1:7090/logs").json()
                self.logs[id] = logs
            except Exception:
                pass
            time.sleep(1)


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

    def add_CT_to_queue(self,tasks_array):
        for task in tasks_array:
            try:
                self.getStatus.queue.put(task.id, False, 60.0)
            except Exception:
                print("Task: " + task.id + " not loaded to queue.")

    def get_last_CT_logs(self,id):
        try:
            return self.getStatus.logs[id]
        except Exception:
            return ['']

