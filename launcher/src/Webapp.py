from launcher.src import app, applications, cockpit, rack, api_app, application
from flask import request, render_template, abort, redirect, session
from flask_restplus import Resource
import json
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, Timeout, MissingSchema

from .model.ComputationTask import ComputationTask,FormEntry,InputDataEntry
from .model.Application import AppInfo
from .application.Launcher import Launcher
from functools import wraps
from .__init__ import auth0
from flask import url_for
from six.moves.urllib.parse import urlencode


launcher = Launcher()

#Config
default_logger = 'https://default-logger.logger.balticlsc'
machine_manager = "https://enigmatic-hollows-51365.herokuapp.com"
mm_path = "/machine-manager/launcher/computations"


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
        apps = launcher.downloader.downloadAppData(path)
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
        task = launcher.ct_manager.getOneCT(id).__str__()
        return task

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
        apps = launcher.downloader.downloadAppData(path)
        json_data = []
        for a in apps:
            json_data.append(a.__repr__().__str__())
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


@app.route('/launcher/app-user/<string:app_id>/createComputationTask')
def showComputationInputForm(app_id):
    #TODO getting form schema from UserApps based on app_id
    #Example schema:
    exampleSchema = []

    for a in launcher.UserApps:
        if a.id == app_id:
            print("App Found")
            exampleSchema = a.getSchema()

    formEntries = []
    for entry in exampleSchema:
        formEntry = FormEntry(entry['name'], entry['type'], entry['defaultValue'])
        formEntries.append(formEntry)

    return render_template('inputForm.html', entryList=formEntries, appID=app_id, userName=launcher.Username)


def return_teapot():
    abort(418, description="I'm a teapot")


""" @app.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        _username = request.form['login']
        print(_username)
        _password = request.form['password']
        if (launcher.verify_password(launcher.hash_password('pass'), _password) and _username[:-1] == 'userT7_') | (launcher.verify_password(launcher.hash_password('pass'), _password) and _username[:-1] == 'userT8_'):
            session['username'] = _username
            launcher.Username = _username
            # Chwilowo brak bazy userów więc hardkodowane UserID
            launcher.UserID = _username[-1]
            return redirect('/launcher')
        return render_template('preSignInMessage.html', message='Invalid username or password',
                                link='/signIn')   
    else:
        pass """



#############-----Auth0------###############

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/signIn')
    return f(*args, **kwargs)

  return decorated


@app.route('/signIn')
def signIn():
        return auth0.authorize_redirect(redirect_uri='https://plan-b-po-launcher.herokuapp.com/callback')


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    launcher.Username = session['profile']['name']
    launcher.UserID = session['profile']['user_id']
    return redirect('/launcher')


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': 'https://plan-b-po-launcher.herokuapp.com/signIn', 'client_id': '1xL7s3OaXnI0mpu3zdCeKQ9nhK8CGiHK'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

#############----------------###############

""" @app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/signIn') """

@app.route('/launcher')
@app.route('/launcher/computation-cockpit')
@requires_auth
def computation_cockpit():
    """ launcher.UserID = UserID
    launcher.Username = Username """
    cts = launcher.ct_manager.getUserCT(launcher.UserID)
    if not cts:
        cts = []
    launcher.downloader.add_CT_to_queue(cts)
    for i in range(cts.__len__()):
        if cts[i].input['logger'] == default_logger or cts[i].input['logger'] == '':
            cts[i].input['logger'] = 'default'
        cts[i].logs = launcher.downloader.get_last_CT_logs(cts[i].id)
    launcher.UserApps = launcher.downloader.downloadAppData(path)
    return render_template("cockpit.html", ctList=cts, appList=launcher.UserApps, userName=launcher.Username)

@app.route("/retake/login/for/user")
@requires_auth
def username():
    return launcher.Username

@app.route('/launcher/app-user/computations', methods=['GET','POST'])
@requires_auth
def computations_manager_endpoint():
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


@app.route('/launcher/app-user/ctOverview/<string:opt>/<int:task_id>')
@requires_auth
def computation_task_activate(opt,task_id):
    task = launcher.ct_manager.getOneCT(task_id)
    if opt == "activate":
        logger = task.input['logger']
        if logger == default_logger:
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
    

@app.route('/launcher/app-user/<string:opt>/<string:task_id>')
@requires_auth
def post_CT(opt,task_id):
    task = launcher.ct_manager.getOneCT(task_id)
    if opt == 'activate':
        logger = task.input['logger']

        try:
            resp = requests.get(logger)
        except (ConnectionError, Timeout, ConnectionError, ConnectTimeout, MissingSchema):
            if not logger == default_logger:
                return render_template("message.html", message="Unable to connect logger!",
                                    link="/launcher/computation-cockpit", userName=launcher.Username)
        ct_to_post = task.__str__()
        try:
            resp = requests.post(machine_manager + mm_path, data=ct_to_post, headers={'Content-type': 'application/json'})
            print(resp.url)
            print(resp.status_code)
            try:
                print(resp.text)
                print(resp)
            except Exception:
                print("Error occured while fetching resp data")
            if resp.status_code == 201 or resp.status_code == 200:
                resp_dict = json.loads(resp.text)
                print(resp_dict['id'])
                launcher.ct_manager.updateCT(task_id, resp_dict['id'])
                return render_template("message.html", message="Computation Activated!",
                                       link="/launcher/computation-cockpit", userName=launcher.Username)
            elif False & (resp.status_code == 401): #lock added for docs policies
                return render_template("message.html", message="You cannot activate running application!",
                                       link="/launcher/computation-cockpit", userName=launcher.Username)
            elif resp.status_code == 404:
                return render_template("message.html", message="Machine Manager: No machine avilable to run your task.",
                                       link="/launcher/computation-cockpit", userName=launcher.Username)
        except (ConnectionError, Timeout, ConnectionError, ConnectTimeout):
            print("Failure during fetching data")
        return render_template("message.html", message="Machine Manager is not working properly", link="/launcher/computation-cockpit", userName=launcher.Username)
    if opt == 'abort':
        try:
            resp = requests.delete(machine_manager+mm_path+'/'+task_id)
            print(resp)
            if (resp.status_code == 200) | (resp.status_code == 202):
                return render_template("message.html", message=task.name + " has been aborted.",
                                    link="/launcher/computation-cockpit", userName=launcher.Username)
            elif (resp.status_code == 201):
                return render_template("message.html", message=task.name + " hasn’t been activated",
                                       link="/launcher/computation-cockpit", userName=launcher.Username)
            elif (resp.status_code == 501):
                return render_template("message.html", message="Machine Manager: Machine reported fatal error with no reasons.\n"
                                                               "Aborting task failed after sending Termination to end worker.",
                                       link="/launcher/computation-cockpit", userName=launcher.Username)
            print("We are in the deeeep end.")
            return render_template("message.html", message=task.name + " hasn’t been activated",
                                link="/launcher/computation-cockpit", userName=launcher.Username)
        finally:
            print("Request is dead as aborted")
            return render_template("message.html", message=task.name + " hasn’t been activated",
                                link="/launcher/computation-cockpit", userName=launcher.Username)
    return "OK", 200



@app.route("/cannot-connect-logger")
def logger_not_exists():
    return render_template("message.html", message="Cannot connect to logger!", userName=launcher.Username)


#Thread-based async logs getter, for test/ not working
@app.route('/log/status')
def get_current_logs():
    print('data')
    return "Not ok", 421

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


