#from collections import OrderedDict

import csv
import codecs
import cStringIO
from datetime import datetime

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

resultFile3 = open("uat_list_with_uris"+timestamp+".csv",'wb')
resultFile2 = open("uat_list"+timestamp+".csv",'wb')
resultFile = open("uat_list_with_alts"+timestamp+".csv",'wb')

wr = UnicodeWriter(resultFile,dialect='excel',quoting=csv.QUOTE_ALL)
wr2 = UnicodeWriter(resultFile2,dialect='excel',quoting=csv.QUOTE_ALL)
wr3 = UnicodeWriter(resultFile3,dialect='excel',quoting=csv.QUOTE_ALL)

wr.writerow(["preferred term"]+["alternate terms"])
wr3.writerow(["preferred term"]+["uri"])

alltermlist = []
for iall in allconcepts:
    alternate = getaltterms(iall)
    altlist = []
    if alternate != None:
        for i in alternate:
            altlist.append(i)
    else:
        altlist = []
    lits = lit(iall)
    wr.writerow([lits]+altlist)
    wr2.writerow([lits])
    wr3.writerow([lits]+[iall])

resultFile.close()
resultFile2.close()
resultFile3.close()

print "Finished. See uat_list"+timestamp+".csv and uat_list_with_alts"+timestamp+".csv"