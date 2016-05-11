import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['techlab-db']

def write( document ):
    db.radio_logs.insert(document)

def read( document ):
    c = db.radio_logs.find(document).count()
    f = db.radio_logs.find(document)
    return c, f

def close():
    client.close()
