from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient("mongodb://CTDatabaseUser:plan-b-po@ctcluster-ph4yr.mongodb.net/CTDatabase")
#app.config['MONGOALCHEMY_DATABASE'] = 'CTDatabase'
#app.config['MONGOALCHEMY_USER'] = 'CTDatabaseUser'
#app.config['MONGOALCHEMY_PASSWORD'] = 'plan-b-po'
#app.config['MONGOALCHEMY_PORT'] = 27017
#app.config['MONGOALCHEMY_SERVER'] = "mongodb+srv://CTDatabaseUser:plan-b-po@ctcluster-ph4yr.mongodb.net/test?retryWrites=true&w=majority"
#db = MongoAlchemy(app)

from launcher.src import Webapp