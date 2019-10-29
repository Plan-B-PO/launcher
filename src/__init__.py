from flask import Flask
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'CTDatabase'
db = MongoAlchemy(app)

from src import Webapp