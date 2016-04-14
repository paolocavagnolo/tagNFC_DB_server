#!/bin/bash
clear
echo "soci to csv"
cd /home/pi/Documents/Database/
rake ohana:csv[https://docs.google.com/spreadsheets/d/1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380/edit?usp=sharing]

echo "csv to json"
python /home/pi/Documents/Database/csv/import_csv.py

echo "json to mongoDB"
mongoimport --db techlab --collection soci --drop --file /home/pi/Documents/Database/out.json
