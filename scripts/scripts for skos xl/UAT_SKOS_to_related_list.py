# coding: utf-8

import codecs
import cStringIO
import csv

#UnicodeWriter from http://docs.python.org/2/library/csv.html#examples
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

#/end UnicodeWriter

resultFile = open("relations"+timestamp+".csv",'wb')
wr = UnicodeWriter(resultFile,dialect='excel',quoting=csv.QUOTE_ALL)

wr.writerow(['.'])


for term in allconcepts:
    print "TERM: "+lit(term).encode('utf-8')
    rts = getrelatedterms(term)
    if rts == None:
        pass
    else:
        print rts
        for rt in rts:
            print rt
            print "RT: "+lit(rt)
            wr.writerow([lit(term)]+["is related to"]+[lit(rt)])


resultFile.close()
print 'finished getting data, look at checkaffil.csv'
# #a function to travel all the way down each path in the thesarus and return this information into a list.
# def descend(term, parents, out_list):
#     lvln = getnarrowerterms(term)
#     if lvln != None: #if there are narrower terms...
#         for a in lvln:
#             children = parents[:]
#             if lit(a) in deprecated:
#                 children = parents[:]
#                 children.append(lit(term))
#                 if children not in out_list:
#                     out_list.append(children)
#             else:
#                 children.append(lit(term))
#                 if children not in out_list:
#                     out_list.append(children)
#                 descend(a, children, GLOBAL_OUT_LIST)
#     else: #if there are no more narrower terms...
#         children = parents[:]
#         children.append(lit(term))
#         if children not in out_list:
#             out_list.append(children)

# print "Organizing the terms..."
# #runs the functions across all terms and outputs to pandas dataframe.
# GLOBAL_OUT_LIST = []
# out_list = []
# for term in alltopconcepts:
#     descend(term, [],GLOBAL_OUT_LIST)
# out_df = pd.DataFrame.from_dict(GLOBAL_OUT_LIST)

# t_out_list = []
# for term in alltopconcepts:
#     descend(term, [], t_out_list)
# print t_out_list

# #counts the number of columns in the data frame and creates the header row.
# numofcol = len(out_df.columns)
# colnames = []
# for i in range(1,numofcol+1):
#     col = 'level '+str(i)
#     colnames.append(col)
# out_df.columns = [colnames]

# #sorts the resulting csv file alphabetically
# out_df_final = out_df.sort(colnames)

# #utf-8-sig encoding fixs umlauts, etc, in the output csv.
# out_df_final.to_csv('uat'+timestamp+'.csv', encoding='utf-8-sig',index=False)

# print "Finished. See uat.csv"