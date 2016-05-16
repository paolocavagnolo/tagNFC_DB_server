import gdrive_mod as excel
import mongodb_mod as db

#read a line
linea = db.read_one()
titoli = excel.read_row_log(1)

#match key with column
j = 0
for item in linea:
    print "guardo %r" % item,
    for titolo in titoli:
        print "e lo confronto con %r" % titolo
        j++
        if item == titolo:
            excel.write_log(2,j,linea[item])
    j = 0


#write
