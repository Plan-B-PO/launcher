from flask import Flask
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'CTDatabase'
app.config['MONGOALCHEMY_USER'] = 'CTDatabaseUser'
app.config['MONGOALCHEMY_PASSWORD'] = 'plan-b-po'
app.config['MONGOALCHEMY_PORT'] = 27017
app.config['MONGOALCHEMY_SERVER'] = 'mongodb://ctcluster-ph4yr.mongodb.net'
db = MongoAlchemy(app)

from launcher.src import Webapp