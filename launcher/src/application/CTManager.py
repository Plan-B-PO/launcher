from launcher.src.model.ComputationTask import ComputationTask
from launcher.src import db
import requests
import json

class CTManager:
    def __init__(self):
        self.document_manager = db.CTDatabase.ComputationTasks
        self.machine_tasks = db.CTDatabase.TaskIDFromMachine

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
                        formInfo[validationName] = int(formInfo[validationName])
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
        ct = {}
        ct['id'] = self.document_manager.find().count().__str__()
        ct['userId'] = UserID
        ct['name'] = ctName
        ct['application'] = appInfoDict
        ct['input'] = {}
        ct['input']['logger'] = ctLogger
        ct['input']['properties'] = formInfo
        ct['mm_ct_id'] = ""

        self.saveCT(ct)
        return ct

    def updateCT(self, ct_id, mm_ct_id):
        try:
            computation_task = self.document_manager.find_one({"id": ct_id})
            computation_task['mm_ct_id'] = mm_ct_id
            self.document_manager.save(computation_task)
        except Exception:
            return False

    def saveCT(self, ct):
       self.document_manager.insert_one(ct)


    def getUserCT(self, userID):
        try:
            computation_tasks = self.document_manager.find({"userId": userID})
            tasks = []
            for i in computation_tasks:
                tasks.append(ComputationTask(
                    id=i['id'],
                    name=i['name'],
                    user_id=i['userId'],
                    application=i['application'],
                    input=i['input'],
                    mm_ct_id=i['mm_ct_id']
                ))
            return tasks
        except Exception:
            return False


    def getOneCT(self, taskID):
        task = self.document_manager.find_one({'id': taskID.__str__()})
        return ComputationTask(
            id=task['id'],
            name=task['name'],
            user_id=task['userId'],
            application=task['application'],
            input=task['input'],
            mm_ct_id=task['mm_ct_id']
        )

    def getAllCT(self):
        tasks = self.document_manager.find({})
        for i in range(tasks.__len__()):
            try:
                id = self.machine_tasks.find_one({'id': i['id'].__str__()})['machine_ones'].__str__()
                resp = json.loads(requests.get("https://enigmatic-hollows-51365.herokuapp.com/machine-manager/launcher/computations"+id).json())
                resp=resp['statuss']
                tasks[i].status = resp
            except Exception:
                pass
        return tasks

    def add_task_id_from_CT(self,ct_id,id_from_machine):
        try:
            task = self.machine_tasks.find_one({'id': ct_id.__str__()})
            task['machine_ones']=id_from_machine.__str__()
            self.machine_tasks.save(task)
        except Exception:
            task = {}
            task['id']=ct_id.__str__()
            task['machine_ones']=id_from_machine.__str__()
            self.machine_tasks.insert_one(task)

    def get_task_status(self,id):
        return self.machine_tasks.find_one({'id': id.__str__()})['machine_ones'].__str__()

    def set_task_status(self, id, status):
        try:
            task = self.machine_tasks.find_one({'id': id.__str__()})
            task['machine_ones'] = status
            self.machine_tasks.save(task)
        except Exception:
            print("Status not changed properly")

    def add_task_status(self,id, status):
        try:
            task = self.machine_tasks.insert_one({'id': id.__str__()})
            task['machine_ones'] = status
            self.machine_tasks.save(task)
        except Exception:
            print("Status not changed properly")