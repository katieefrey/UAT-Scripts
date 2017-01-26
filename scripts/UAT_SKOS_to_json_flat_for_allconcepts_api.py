from collections import OrderedDict

alltermlist = []

for iall in allconcepts:
    alltermdict = {}
    alltermdict['prefLabel'] = lit(iall)
    alltermdict['@id'] = "http://uat.altbibl.io/term/"+lit(iall).replace(" ","_")
    alltermdict['hasStatus'] = getvocstatus(iall)

    alternate = getaltterms(iall) 
    if alternate != None:
        altdict = {}
        altlist= []

        for i in alternate:
            altlist.append(i)
            alltermdict['altLabel'] = altlist
        alltermlist.append(alltermdict)

    else:
        alltermlist.append(alltermdict)

print len(alltermlist)
sortedlist = sorted(alltermlist, key=lambda k: k['prefLabel']) 


timestamp = "2015_0821_1038"
month = timestamp[5:7]
day = timestamp[7:9]
hours = timestamp[10:12]+":"+timestamp[12:14]
year = timestamp[:4]
months = {'01':'January', '08': 'August'}

def findmonth(month):
    for key, value in months.items():
        if key == month:
            return value

writtentime = findmonth(month)+" "+day+" "+year+", "+hours

finaldict = {
    "alphauat": sortedlist,
    "timestamp":writtentime
}


js_file = open("uat_flat_api.json", "wb")
js_file.write(json.dumps(finaldict))
js_file.close()

print "Finished. See uat_flat_api.json. Don't forget to give it a version name!!!"