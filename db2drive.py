import gdrive_mod as excel
import mongodb_mod as db

#read a line
linea = db.read_one()
titoli = excel.read_raw_log(1)

#match key with column
for item in linea:
    print "guardo %r" % item,
    for titolo in titoli:
        print "e lo confronto con %r" % titolo



#write
