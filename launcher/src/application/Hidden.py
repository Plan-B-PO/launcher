import queue
import time
import threading

class App:
    logs = []
    status = ''
    queue = queue.Queue(1024)
    archi_test = [
        'APP STARTED',
        'APP COMPLETED'
    ]
    steps0 = [
        '',
        '',
        '',
        '',
        ''
    ]
    steps1 = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ]

    def __init__(self, ct_id):
        self.ct_id = ct_id

    def thread_method(self, app_name):
        self.status = 'IN PROGRESS'
        app_size = 5
        if app_name == '1':
            app_size = 10
        if not self.logs[self.ct_id]:
            self.logs[self.ct_id] = []
        print('debug1')
        if app_name == 'patryk_testowy':
            for i in range(2):
                time.sleep(1)
                self.logs[self.ct_id].append(self.archi_test[i])
                time.sleep(25)
            print('debug2')
        else:
            for i in range(app_size):
                if app_name == '1':
                    self.logs[self.ct_id].append(self.steps1[i])
                else:
                    self.logs[self.ct_id].append(self.steps0[i])
                time.sleep(0.5)
            print('debug2')
        print('debug3')
        self.status = 'DONE'


class AppRunner:
    apps = []
    threads = {}
    ids = []

    def get_app_state(self, ct_id):
        try:
            for app in self.apps:
                if app.ct_id == ct_id:
                    return app.status
        except Exception:
            return ''

    def run_new_app(self, ct_id, app_name):
        if not (ct_id in self.ids):
            self.ids.append(ct_id)
            app = App(ct_id)
            self.apps.append(app)
            try:
                self.threads[ct_id] = threading.Thread(app.thread_method(app_name))
                self.threads[ct_id].start()
            except Exception:
                pass

    def run_app(self,ct_id , app_name):
        try:
            for app in self.apps:
                if app.ct_id == ct_id:
                    self.threads[ct_id] = threading.Thread(app.thread_method(app_name))
                    self.threads[ct_id].start()
        except Exception:
            pass

    def get_logs_of_app(self, ct_id):
        try:
            for app in self.apps:
                if app.ct_id == ct_id:
                    return app.logs
        except Exception:
            return []

    def end_app(self, ct_id):
        try:
            for app in self.apps:
                if app.ct_id == ct_id:
                    return
        except Exception:
            return []

    def run_thread(self):
        self.thread = threading.Thread(target=self.getStatus.thread_method)
        self.thread.start()
