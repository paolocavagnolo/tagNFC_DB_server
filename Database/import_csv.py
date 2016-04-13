import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
#CSV to JSON Conversion
csvfile = open('C://test//final-current.csv', 'r')
reader = csv.DictReader( csvfile )
mongo_client=MongoClient()
db=mongo_client.october_mug_talk
db.segment.drop()
header= [ "Tessera", "tagNFC", "Data richiesta", "Data accettazione", "Tutore", "Mail", "Nome", "Cognome", "Data nascita", "Luogo nascita", "Residenza", "CF", "Qualifica", "Quota 2015" ,"Quota 2016", "Data annullamento"]

for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.segment.insert(row)
