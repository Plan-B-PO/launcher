from flask import Flask
from flask import request
import requests
import json

from Mod import Downloader, Launcher, AppInfo, CTManager

app = Flask(__name__)

launcher = Launcher()

#Temporary dummy data
path = "/library/launcher/applications"
UserID = 123
Username = "TestName"

AppInfo = {
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
}


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
