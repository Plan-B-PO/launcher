from flask import Flask
from flask import request, render_template
import requests
import json

from .Mod import Downloader, Launcher, AppInfo, CTManager, FormEntry

app = Flask(__name__)

launcher = Launcher()

#Temporary dummy data
path = "/library/launcher/applications"
UserID = 123
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

@app.route('/launcher/app-user/computations', methods=['POST'])
def handleCT():
    launcher.postComputations(request.form)


##################----EXPERIMENTS----####################


@app.route('/launcher/app-user/application/<int:app_id>')
def showAppDetails(app_id):
    #TODO currentAppInfo = launcher.UserApps where id=app_id
    #Example currnetAppInfo
    currentAppInfo = AppInfo(123, 'Awful App', 'Really awful application', 'noicon')
    return render_template('appDetails.html', appID=currentAppInfo.id, appName=currentAppInfo.name, 
                                        appDescription=currentAppInfo.description, appIcon=currentAppInfo.icon)

@app.route('/launcher/app-user/<int:app_id>/createComputationTask')
def showComputationInputForm(app_id):
    #TODO downloading form schema based on app_id
    #Example schema:
    exampleSchema = [
                        {
                            "name": 'Zmienna X',
                            "type": "int",
                            "defaultValue": 1,
                        },

                        {
                            "name": 'Zmienna Y',
                            "type": "int",
                            "defaultValue": 2,
                        },

                        {
                            "name": 'Zmienna Z',
                            "type": "int",
                            "defaultValue": 3,
                        }
    ]

    formEntries = []
    for entry in exampleSchema:
        formEntry = FormEntry(entry['name'], entry['type'], entry['defaultValue'])
        formEntries.append(formEntry)

    return render_template('inputForm.html', entryList=formEntries)