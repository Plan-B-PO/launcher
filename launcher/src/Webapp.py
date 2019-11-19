from launcher.src import app
from flask import request, render_template, abort
import json
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, Timeout, MissingSchema

from .Mod import Downloader, Launcher, AppInfo, FormEntry, InputDataEntry



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
            return render_template('message.html', message=message,link="/launcher/computation-cockpit")
        else:
            return render_template('message.html', message='Invalid input data - abort', link="/launcher/computation-cockpit")
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


def return_500():
    abort(418, description="I'm a teapot")

@app.route('/')
@app.route('/launcher/computation-cockpit')
def computation_cockpit():
    a = launcher.ct_manager.getUserCT("123")
    return render_template("cockpit.html", ctList=a)


@app.route('/launcher/app-user/ctOverview/<string:opt>/<int:task_id>')
def computation_task_activate(opt,task_id):
    task = launcher.ct_manager.getOneCT(task_id)
    if opt == "activate":
        logger = json.loads(task.input)['logger']
        if logger == 'https://default-logger.logger.balticlsc':
            logger = "default"
        app_id = json.loads(task.application)['id']
        input_data = json.loads(task.input)['properties']
        data = []
        for key,value in input_data.items():
            data.append(
                InputDataEntry(key,value)
            )
        return render_template("actionOverview.html", task=task,actionType=opt, logger=logger, app=app_id, titleString=opt + " " + task.name, ctList=data)
    elif opt == "abort":
        return render_template("question.html", message="Are you sure, you want to abort \"" + task.name + "\"?", link_yes="/launcher/app-user/abort/"+task_id.__str__(), link_no="/launcher/computation-cockpit")
    return "Not implemented", 500


@app.route('/launcher/app-user/<string:opt>/<int:task_id>')
def post_CT(opt,task_id):
    task = launcher.ct_manager.getOneCT(task_id)
    if opt == 'activate':
        logger = json.loads(task.input)['logger']
        if logger == 'https://default-logger.logger.balticlsc':
            logger = "https://www.google.com"
        try:
            resp = requests.get(logger)
        except (ConnectionError, Timeout, ConnectionError, ConnectTimeout, MissingSchema):
            return render_template("message.html", message="Unable to connect logger!", link="/launcher/computation-cockpit")
        ct_to_post = {}
        ct_to_post['computation_task'] = task.__repr__()
        ct_to_post['version'] = -1
        try:
            resp = requests.post("http://localhost:5000/machine-manager/launcher/computations",json=json.dumps(ct_to_post))
        except (ConnectionError, Timeout, ConnectionError, ConnectTimeout):
            return "I'm a teapot.", 418

        if resp.status_code == 200:
            return render_template("message.html", message="Computation Activated!", link="/launcher/computation-cockpit")
        elif resp.status_code == 400:
            return render_template("message.html", message="Computation Not Activated!", link="/launcher/computation-cockpit")
        return "I'm a teapot.", 418
    if opt == 'abort':
        try:
            resp = requests.delete("http://localhost:5000/machine-manager/launcher/computations/"+task_id)
            if resp.status_code == 200:
                return render_template("message.html", message=task.name + " has been aborted.",
                                       link="/launcher/computation-cockpit")
            return render_template("message.html", message=task.name + " hasn’t been activated",
                                   link="/launcher/computation-cockpit")
        finally:
            return "I'm a teapot.", 418

    return "OK", 200


x = False
@app.route('/machine-manager/launcher/computations')
def smth():
    global x
    if x:
        x = False
        return "OK", 200
    else:
        x = True
        return "NOT OK", 400


@app.route("/cannot-connect-logger")
def logger_not_exists():
    return render_template("message.html", message="Cannot connect to logger!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
