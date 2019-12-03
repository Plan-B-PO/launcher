from launcher.src.model.ComputationTask import ComputationTask
from launcher.src import db


class CTManager:
    def __init__(self):
       self.document_manager = db.CTDatabase.ComputationTasks

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

        self.saveCT(ct)
        return ct

    def saveCT(self, ct):
       self.document_manager.insert_one(ct)


    def getUserCT(self, userID):
        computation_tasks = self.document_manager.find({"userId": userID})
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

    def getOneCT(self ,taskID):
        task = self.document_manager.find_one({"id" :taskID})
        return ComputationTask(
            id=task['id'],
            name=task['name'],
            user_id=task['userId'],
            application=task['application'],
            input=task['input'])

    def getAllCT(self):
        return self.document_manager.find({})