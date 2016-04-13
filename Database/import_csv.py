import csv, simplejson, decimal, codecs

data = open("soci.csv")
reader = csv.DictReader(data, delimiter=",", quotechar='"')

with codecs.open("out.json", "w", encoding="utf-8") as out:
    for r in reader:
        for k, v in r.items():
         # make sure nulls are generated
         if not v:
            r[k] = None
         # generate int
        elif k == "Tessera":
            r[k] = int(v)
        out.write(simplejson.dumps(r, ensure_ascii=False, use_decimal=True)+"\n")
