import pymongo
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['techlab-db']

def close():
    client.close()

def write( document ):
    db.radio_logs.insert(document)

def read( document ):
    c = db.radio_logs.find(document).count()
    f = db.radio_logs.find(document)
    return c, f

def read_one():
    return db.radio_logs.find_one()

def read_last():
    tutti = db.radio_logs.find().skip(db.collection.count() - 100)
    for item in tutti:
        return item
