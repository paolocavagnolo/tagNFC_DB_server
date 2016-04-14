import csv, simplejson, decimal, codecs

data = open("/home/pi/Documents/Database/csv/soci.csv")
reader = csv.DictReader(data, delimiter=",", quotechar='"')

with codecs.open("/home/pi/Documents/Database/out.json", "w", encoding="utf-8") as out:
    for r in reader:
        for k, v in r.items():
            if not v:
                r[k] = None

    out.write(simplejson.dumps(r, ensure_ascii=False, use_decimal=True)+"\n")
