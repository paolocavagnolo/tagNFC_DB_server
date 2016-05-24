import pymongo
from pymongo import MongoClient

CLIENT = 'mongodb://paolocavagnolo:q22q22q22@ds011943.mlab.com:11943/techlab'

class mongoDB(object):

    def __init__(self, collection, database):
        self.client = MongoClient(CLIENT)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def close(self):
        self.client.close()

    def read(self, document):
        c = self.collection.find(document).count()
        f = self.collection.find(document)
        return c, f

    def write(self, document):
        return self.collection.insert_one(document).inserted_id

    def read_last_N(self, N):
        alls = self.collection.find().skip(self.collection.count() - N)
        malloppo = []
        for item in alls:
            malloppo.append(item)
        return malloppo

    
