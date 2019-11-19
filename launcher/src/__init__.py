from flask import Flask
from flask_mongoalchemy import MongoAlchemy
import pymongo
from pymongo import MongoClient
#mongo client is connected
client = MongoClient()
db     = client['db']

app = Flask(__name__)
#app.config['MONGOALCHEMY_DATABASE'] = 'CTDatabase' #'mongodb://127.0.0.1:27017/data/db/CTDatabase'
#app.config['MONGOALCHEMY_SERVER'] = 'mongo'
#app.config['MONGOALCHEMY_PORT'] = '27017'
#db = MongoAlchemy(app)

from launcher.src import Webapp