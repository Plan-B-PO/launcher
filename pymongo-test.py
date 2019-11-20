import pymongo
import urllib.parse

MONGO_HOST = urllib.parse.quote('mongodb://ctcluster-shard-00-01-ph4yr.mongodb.net')
MONGO_PORT = 27017
MONGO_DB = urllib.parse.quote('CTDatabase')
MONGO_USER = urllib.parse.quote_plus('CTDatabaseUser')
MONGO_PASS = urllib.parse.quote_plus('plan-b-po')

client = pymongo.MongoClient("mongodb+srv://"
                             + MONGO_USER
                             + ":" + MONGO_PASS
                             + "@ctcluster-ph4yr.mongodb.net/test?retryWrites=true&w=majority")
session = client.start_session()
db = client.test
print(db)
print(client.list_database_names(session))
