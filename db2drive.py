import gdrive_mod as excel
import mongodb_mod as db

#read the first line
titoli = excel.read_row_log(1)

#match key with column
def update_linea( row , linea):
    j = 0
    for item in linea:
        print "guardo %r" % item,
        for titolo in titoli:
            print "e lo confronto con %r" % titolo
            j = j + 1
            if item == titolo:
                excel.write_log(row,j,linea[item])

#
l = db.read_last()
print l
