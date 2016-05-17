import gdrive_mod as excel
import mongodb_mod as db

# read the first line
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


records = db.read_last_N(100)

l = 1

for document in records:
    print document
    print l
    l = l + 1
    #update_linea(l, document)
