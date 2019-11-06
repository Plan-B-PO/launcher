from launcher.src import app
from flask import request, render_template, abort
import json

from .Mod import Downloader, Launcher, AppInfo, FormEntry



launcher = Launcher()

#Temporary dummy data
path = "/library/launcher/applications"
UserID = "123"
Username = "TestName"

""" AppInfo = {
    "id": 1234,
    "name": "SuperApp1",
    "description": "This app allows multiplying large matrices",
    "icon": "https://imgur.com/exapmle1"
}

formInfo = {
    "name": "testname",
    "param1": "xxx",
    "param2": "yyy",
    "logger": "loggertest"
} """


@app.route('/launcher/app-user/applications')
def showApps():
    downloader = Downloader()
    apps = downloader.downloadAppData(path)
    launcher.UserID = UserID
    launcher.Username = Username
    launcher.UserApps = apps
    #TODO

@app.route('/launcher/app-user/computations', methods=['POST','GET'])
def handleCT():
    if request.method == 'POST':
        # Na ten moment endpoint z funkcją w której launcherowi przypisywany jest UserID jest nieużywany więc
        # przypisujemy poniżej
        launcher.UserID = UserID
        #createCTStatusOK = launcher.postComputations(request.form)
        createdCTName = launcher.postComputations(request.form)
        if createdCTName:
            message = 'Computation Task "' + createdCTName + '" created'
            return render_template('message.html', message=message)
        else:
            return render_template('message.html', message='Invalid input data - abort')
    elif request.method == 'GET':
        user_cts = launcher.ct_manager.getUserCT(UserID)
        json_data = []
        for a in user_cts:
            json_data.append({"name":a.name,
                             "id":a.id})
        return json.dumps(json_data)




##################----EXPERIMENTS----####################


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


@app.route('/launcher/app-user/application/<int:app_id>')
def showAppDetails(app_id):
    #TODO currentAppInfo = launcher.UserApps where id=app_id
    #Example currnetAppInfo:
    currentAppInfo = AppInfo(123, 'Test App 01', 'Really awful application', 'noicon', dummySchema)
    return render_template('appDetails.html', appID=currentAppInfo.id, appName=currentAppInfo.name, 
                                        appDescription=currentAppInfo.description, appIcon=currentAppInfo.icon)


@app.route('/launcher/app-user/<int:app_id>/createComputationTask')
def showComputationInputForm(app_id):
    #TODO getting form schema from UserApps based on app_id
    #Example schema:
    exampleSchema = dummySchema

    formEntries = []
    for entry in exampleSchema:
        formEntry = FormEntry(entry['name'], entry['type'], entry['defaultValue'])
        formEntries.append(formEntry)

    return render_template('inputForm.html', entryList=formEntries, appID=app_id)

@app.route('/')
def return_500():
    abort(418, description="I'm a teapot")


@app.route('/launcher/computation-cockpit')
def computation_cockpit():
    return render_template("cockpit.html")


@app.route('/launcher/computation-task/<int:task_id>/abort')
def computation_task_abort(task_id):
    return render_template("computationDetails.html", message="Are you sure, you want to abort \"Test Task " + task_id.__str__() + "\"?")


@app.route('/launcher/computation-task/<int:task_id>/activate')
def computation_task_activate(task_id):
    logger = "default"
    if task_id == 2:
        logger = "https://non-existing-logger.com"

    return render_template("activate.html", logger=logger)


@app.route("/cannot-connect-logger")
def logger_not_exists():
    return render_template("message.html",message="Cannot connect to logger!")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)