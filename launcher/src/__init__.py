from flask import Flask, Blueprint
from flask_restplus import Api
from pymongo_helplib import MongoClient
import os

app = Flask(__name__)
""" app.config.from_pyfile('config.cfg') """
app.secret_key = os.environ['SECRET_KEY']
blueprint = Blueprint('api', __name__, url_prefix='/api')
api_app = Api(app = app,blueprint=blueprint, doc='/doc/', version = "0.0", title = "Launcher", description = "API for launcher")

applications = api_app.namespace("launcher/app-user/applications", description="Applications from Library")
application = api_app.namespace("launcher/app-user/application", description="Applications from Library")
cockpit = api_app.namespace("launcher/app-user/cockpit", description="Computation Cockpit things")
rack = api_app.namespace("launcher/app-user/rack", description="This looks like a cancer")



db = MongoClient("mongodb+srv://ctcluster-ph4yr.mongodb.net/CTDatabase",
                 username='CTDatabaseUser',
                 password='plan-b-po'
                 )

from launcher.src import Webapp