from flask import Flask
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'CTDatabase' #'mongodb://localhost:27017/data/db/CTDatabase'
db = MongoAlchemy(app)

from launcher.src import Webapp