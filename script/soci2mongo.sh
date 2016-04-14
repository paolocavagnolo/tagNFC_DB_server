#!/bin/bash
clear
echo "soci to csv"
cd /home/pi/Documents/Database/
rake ohana:csv[https://docs.google.com/spreadsheets/d/1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380/edit?usp=sharing]

echo "csv to json"
python /home/pi/Documents/Database/csv_json.py -i /home/pi/Documents/Database/csv/soci.csv -o /home/pi/Documents/Database/out.json -f pretty

echo "json to mongoDB"
mongoimport --db techlab --collection soci --drop --file /home/pi/Documents/Database/out.json --jsonArray
