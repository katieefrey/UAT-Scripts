# coding: utf-8

import os
import csv
import json
import shutil
import rdflib
import codecs
import cStringIO
import unicodedata
import pandas as pd
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

print "Reading the SKOS file...this may take a few seconds."

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

##### RDF File Location #####
##### assign this variable to location of UAT SKOS-RDF file exported from VocBench ##### 
rdf = "uat.history-17-01-23.rdf"

##### Shared Functions and Variables #####
##### do NOT edit this section #####
##### scroll down for conversion scripts #####

#reads SKOS-RDF file into a RDFlib graph for use in these scripts
g = rdflib.Graph()
result = g.parse((rdf).encode('utf8'))

#defines certain properties within the SKOS-RDF file
prefLabel = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')
broader = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#broader')
Concept = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#Concept')
vocstatus = rdflib.term.URIRef('http://art.uniroma2.it/ontologies/vocbench#hasStatus')
altLabel = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#altLabel')
TopConcept = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#topConceptOf')
ednotes = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#editorialNote')
changenotes = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#changeNote')
scopenotes = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#scopeNote')
example = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#example')
related = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#related')
oldvalue = rdflib.term.URIRef('http://schema.semantic-web.at/ppt/history#oldValue')
value = rdflib.term.URIRef('http://schema.semantic-web.at/ppt/history#value')
subjectOfChange = rdflib.term.URIRef('http://purl.org/vocab/changeset/schema#subjectOfChange')
createdDate = rdflib.term.URIRef('http://purl.org/vocab/changeset/schema#createdDate')
changeType = rdflib.term.URIRef('http://purl.org/vocab/changeset/schema#changeType')
affLit = rdflib.term.URIRef('http://schema.semantic-web.at/ppt/history#affectedLiteral')
changeorder = rdflib.term.URIRef('http://schema.semantic-web.at/ppt/history#changeOrder')
relres = rdflib.term.URIRef('http://schema.semantic-web.at/ppt/history#relatedResourceLabel')
predtype = rdflib.term.URIRef('http://schema.semantic-web.at/ppt/history#predicate')

#a list of all top concepts
#alltopconcepts = [bv for bv in g.subjects(predicate=TopConcept)]

#a list of all concepts
#allconcepts = [gm for gm in g.subjects(rdflib.RDF.type, Concept)]

#finds all entries that have a "value"
allvalue = [we for we in g.subjects(predicate=value)]
allaffLit = [we for we in g.subjects(predicate=affLit)]

reallyallvals = [we for we in g.subjects(predicate=subjectOfChange)]

#print reallyallvals

alladditions = [we for we in g.subjects(object="REMOVAL")]

#print alladditions
#print allvalue

#help for figuring out what predicates you have to work with
#for s,p,o in g:
#    print s,p,o
#print allvalue

for x in range(0,20):
    y = allaffLit[x]
    print y
    for newvalue in g.objects(subject=rdflib.term.URIRef(y), predicate=value):
        print newvalue

    for afLit in g.objects(subject=rdflib.term.URIRef(y), predicate=affLit):
        print afLit
    
    for previousvalue in g.objects(subject=rdflib.term.URIRef(y), predicate=oldvalue):
        print "this is prev value! "+ previousvalue
        if previousvalue != None:    
            print previousvalue
        else:
            print "blank!"


#newvalue1 = g.objects(subject=rdflib.term.URIRef(allvalue[0]), predicate=value)
#print newvalue1
print "function starting here"

def findallinfo(entry):
    infolist = []
    infolist.append(entry)
    for date1 in g.objects(subject=rdflib.term.URIRef(entry), predicate=createdDate):
        infolist.append(date1)
    for suburi in g.objects(subject=rdflib.term.URIRef(entry), predicate=subjectOfChange):
        infolist.append(suburi)
    for cord in g.objects(subject=rdflib.term.URIRef(entry), predicate=changeorder):
        infolist.append(cord)
    for changet in g.objects(subject=rdflib.term.URIRef(entry), predicate=changeType):
        infolist.append(changet)
    for predt in g.objects(subject=rdflib.term.URIRef(entry), predicate=predtype):
        infolist.append(predt)
    for previousvalue in g.objects(subject=rdflib.term.URIRef(entry), predicate=oldvalue):
        infolist.append(previousvalue)
    for newvalue in g.objects(subject=rdflib.term.URIRef(entry), predicate=value):
        infolist.append(newvalue) 
    for afLit in g.objects(subject=rdflib.term.URIRef(y), predicate=affLit):
        infolist.append(afLit) 
    for rels in g.objects(subject=rdflib.term.URIRef(y), predicate=relres):
        infolist.append(rels) 
    return infolist


#print "Concept "+suburi+" used to be "+previousvalue+" and is now "+newvalue+", this change was made on "+date1+"."


resultFile = open("uat_updates"+timestamp+".csv",'wb')
wr = UnicodeWriter(resultFile,dialect='excel',quoting=csv.QUOTE_ALL)

wr.writerow(["date of change"]+["concept URI"]+["old value"]+["new value"]+["type of change"])





for y in reallyallvals:
    wr.writerow(findallinfo(y))

#for y in allaffLit:
    #wr.writerow(findinfoafflit(y))


resultFile.close()
