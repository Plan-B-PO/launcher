from launcher.src import app, applications, cockpit, rack, api_app, application
from flask import request, render_template, abort, redirect, session
from flask_restplus import Resource
import json
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, Timeout, MissingSchema

from .model.ComputationTask import ComputationTask,FormEntry,InputDataEntry
from .model.Application import AppInfo
from .application.Launcher import Launcher
from .application.Downloader import Downloader


launcher = Launcher()
downloader = Downloader()
downloader.run_thread()

#Temporary dummy data
path = "https://plan-b-po-library.herokuapp.com/library/launcher/applications"#private mock for library
UserID = "123"
Username = "user01"

@application.route('/<string:id>')
class UserApplications(Resource):
    def get(self, id):
        #TODO: set UserID as id
        tasks = launcher.ct_manager.getUserCT(UserID)
        array = []
        for a in tasks:
            array.append(a.__repr__())
        return json.dumps(array)


@applications.route('/')
class Applications(Resource):

    @api_app.doc(responses={200:"OK"})
    def get(self):
        apps = downloader.downloadAppData(path)
        launcher.UserID = UserID
        launcher.Username = Username
        launcher.UserApps = apps
        array = []
        for a in apps:

            print(a.__repr__())
            array.append(a.__repr__())
        print(array)
        return json.dumps(array)
        # TODO


@app.route('/launcher/app-user/computations/<string:id>')
def get_one_computation(id):
        return "OK", 200

@app.route('/launcher/app-user/computations/<string:id>')
def delete_computation(id):
    return "You shall not pass", 400

@app.route('/launcher/app-user/computations/<string:id>/logs')
def get_logs(id):
    return "OK", 200


@cockpit.route("/")
class Cockpit(Resource):

    @api_app.doc(responses={200: "OK"})
    def get(self):
        apps = downloader.downloadAppData(path)
        json_data = []
        for a in apps:
            json_data.append(a.__repr__())
        return "OK", 200, json.dumps(json_data)

    @api_app.doc(responses={201:"Application added"})
    def post(self):
        return "Application added", 201


@cockpit.route("/<int:id>")
class CockpitID(Resource):

    def get(self, id):
        return "OK", 200



@rack.route("/")
class Rack(Resource):

    def get(self):
        return "OK", 200

    def post(self):
        return "OK", 201

@rack.route("/<int:id>")
class RackID(Resource):

    def get(self,id):
        return "OK", 200

    def delete(self,id):
        return "Not Deleted", 419







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


@app.route('/launcher/app-user/application-details/<string:app_id>')
def showAppDetails(app_id):
    #TODO currentAppInfo = launcher.UserApps where id=app_id
    #Example currnetAppInfo:
    currentAppInfo = AppInfo(10001, 'Test App 01', 'Nop test app',
                             'http://blog.nop.ee/wp-content/uploads/2014/05/NOPiLogoPunaneRing-1.jpg', dummySchema)
    for a in launcher.UserApps:
        if a.id == app_id:
            currentAppInfo = a

    return render_template('appDetails.html', appID=currentAppInfo.id, appName=currentAppInfo.name, 
                                        appDescription=currentAppInfo.description, appIcon=currentAppInfo.icon, userName=launcher.Username)


@app.route('/launcher/app-user/<int:app_id>/createComputationTask')
def showComputationInputForm(app_id):
    #TODO getting form schema from UserApps based on app_id
    #Example schema:
    exampleSchema = dummySchema

    formEntries = []
    for entry in exampleSchema:
        formEntry = FormEntry(entry['name'], entry['type'], entry['defaultValue'])
        formEntries.append(formEntry)

    return render_template('inputForm.html', entryList=formEntries, appID=app_id, userName=launcher.Username)


def return_teapot():
    abort(418, description="I'm a teapot")


@app.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        _username = request.form['login']
        _password = request.form['password']
        if launcher.verify_password(launcher.hash_password('pass'), _password) and _username[:-1] == 'userT7_':
            session['username'] = _username
            launcher.Username = _username
            # Chwilowo brak bazy userów więc hardkodowane UserID
            launcher.UserID = _username[-1]
            return redirect('/launcher')
        return render_template('preSignInMessage.html', message='Invalid username or password',
                                link='/signIn')   
    else:
        pass

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/signIn')

@app.route('/launcher')
@app.route('/launcher/computation-cockpit')
def computation_cockpit():
    if session.get('username'):
        """ launcher.UserID = UserID
        launcher.Username = Username """
        cts = launcher.ct_manager.getUserCT(launcher.UserID)
        launcher.UserApps = downloader.downloadAppData(path)
        return render_template("cockpit.html", ctList=cts, appList=launcher.UserApps, userName=launcher.Username)
    else:
        return redirect('/signIn')


@app.route('/launcher/app-user/computations', methods=['GET','POST'])
def computations_manager_endpoint():
    if session.get('username'):
        if request.method == 'GET':
            user_cts = launcher.ct_manager.getUserCT(UserID)
            json_data = []
            for a in user_cts:
                json_data.append(a.__repr__())
            return "Application list", 200, json.dumps(json_data)
        elif request.method == 'POST':
            # Na ten moment endpoint z funkcją w której launcherowi przypisywany jest UserID jest nieużywany więc
            # przypisujemy poniżej
            # createCTStatusOK = launcher.postComputations(request.form)
            # createdCTName = launcher.postComputations(request.form)
            ct = launcher.addComputationTask(request.form)
            if ct:
                message = 'Computation Task "' + ct.name + '" created'
                return render_template('message.html', message=message, link="/launcher/computation-cockpit", userName=launcher.Username)
            else:
                return render_template('message.html', message='Invalid input data - abort',
                                    link="/launcher/computation-cockpit", userName=launcher.Username)
    else:
        return redirect('/signIn')


@app.route('/launcher/app-user/ctOverview/<string:opt>/<int:task_id>')
def computation_task_activate(opt,task_id):
    if session.get('username'):
        task = launcher.ct_manager.getOneCT(task_id)
        if opt == "activate":
            logger = task.input['logger']
            if logger == 'https://default-logger.logger.balticlsc':
                logger = "default"
            app_id = task.application['id']
            input_data = task.input['properties']
            data = []
            for key,value in input_data.items():
                data.append(
                    InputDataEntry(key,value)
                )
            return render_template("actionOverview.html", task=task,actionType=opt, logger=logger, app=app_id, titleString=opt + " " + task.name, ctList=data, userName=launcher.Username)
        elif opt == "abort":
            return render_template("question.html", message="Are you sure, you want to abort \"" + task.name + "\"?", link_yes="/launcher/app-user/abort/"+task_id.__str__(), link_no="/launcher/computation-cockpit", userName=launcher.Username)
        return "Not implemented", 500
    else:
        return redirect('/signIn')

@app.route('/launcher/app-user/<string:opt>/<string:task_id>')
def post_CT(opt,task_id):
    if session.get('username'):
        task = launcher.ct_manager.getOneCT(task_id)
        if opt == 'activate':
            logger = task.input['logger']

            try:
                resp = requests.get(logger)
            except (ConnectionError, Timeout, ConnectionError, ConnectTimeout, MissingSchema):
                if not logger == 'https://default-logger.logger.balticlsc':
                    return render_template("message.html", message="Unable to connect logger!",
                                        link="/launcher/computation-cockpit", userName=launcher.Username)
            ct_to_post = task.__str__()
            try:
                resp = requests.post("https://enigmatic-hollows-51365.herokuapp.com/machine-manager/launcher/computations", data=ct_to_post, headers={'Content-type': 'application/json'})
            except (ConnectionError, Timeout, ConnectionError, ConnectTimeout):
                return "I'm a teapot.", 418


            if resp.status_code == 200:#task.name=="Test Task 01":
                return render_template("message.html", message="Computation Activated!", link="/launcher/computation-cockpit", userName=launcher.Username)
            elif resp.status_code == 400:#task.name=="Test Task 02":
                return render_template("message.html", message="You cannot activate running application!", link="/launcher/computation-cockpit", userName=launcher.Username)
            return "I'm a teapot.", 418
        if opt == 'abort':
            try:
                resp = requests.delete("https://enigmatic-hollows-51365.herokuapp.com/machine-manager/launcher/computations/"+task_id)
                if resp.status_code == 200:
                    return render_template("message.html", message=task.name + " has been aborted.",
                                        link="/launcher/computation-cockpit", userName=launcher.Username)
                return render_template("message.html", message=task.name + " hasn’t been activated",
                                    link="/launcher/computation-cockpit", userName=launcher.Username)
            finally:
                return render_template("message.html", message=task.name + " hasn’t been activated",
                                    link="/launcher/computation-cockpit", userName=launcher.Username)
        return "OK", 200
    else:
        return redirect('/signIn')



@app.route("/cannot-connect-logger")
def logger_not_exists():
    return render_template("message.html", message="Cannot connect to logger!", userName=launcher.Username)


#Thread-based async logs getter
@app.route('/log/status')
def get_current_logs():
    print('data')
    data = downloader.get_last_thread_data()
    print(data)
    return json.dumps(data)

""" @app.route("/logout")
def logout():
    return redirect('/login') """

""" @app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        #TODO: template logowania
        return render_template("message.html", message="Logging in is not implemented", link='/launcher')
    elif request.method == 'POST':
        launcher.Username = request.form['username']
        return redirect('/launcher') """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
