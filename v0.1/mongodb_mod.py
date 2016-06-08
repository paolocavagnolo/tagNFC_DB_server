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

def read_last_N( N ):
    tutti = db.radio_logs.find().skip(db.radio_logs.count() - N)
    malloppo = []
    for item in tutti:
        malloppo.append(item)
    return malloppo

def write_energy( document ):
    db.energy.insert(document)

def read_energy():
    c = db.energy.find(document).count()
    f = db.energy.find(document)
    return c, f
