# This code is for name processing

import sys
import cPickle as pickle
import math

path = "../../ACMdata/"

dicIn = pickle.load(open( path + "authorMatch.dump","r"))

dicHindex = {}

fout = open( path + "HindexAuthorList.txt", "wb")
foutdump = open( path + "HindexAuthorList.dump", "wb")

def isSame(name1,name2):
    if (name1.find(name2)>=0) or (name2.find(name1)>=0): return True
    if (name1.find("&#")>=0) or (name2.find("&#")>=0) or (name1.find(".")>=0) or (name2.find(".")>=0):
        if name1[0:0]==name2[0:0]: return True
    return False

print "Begin Name Processing"
for oname in dicIn:
    candidate = {}
    for tname in dicIn[oname]:
#        print oname,tname
        name1 = oname.strip()
        name2 = tname.strip()
        if name1.find(",")>=0: 
            name1 = name1[0:name1.find(",")]
        if name2.find(",")>=0:
            name2 = name2[0:name2.find(",")]
        name1s = name1.split(" ")
        name1lens = 0
        name1first = ""
        name1last = ""
        for item in name1s:
            if item!="": 
                name1lens += 1
                name1last = item.lower()
            if (name1lens==1) and (item!=""):
                name1first = item.lower()
             
        if name1lens>3: continue     
        name2s = name2.split(" ")
        name2lens = 0
        name2first = ""
        name2last = ""
        for item in name2s:
            if item!="": 
                name2lens += 1
                name2last = unicode(item.lower(),"utf-8",errors="ignore")
            if (name2lens==1) and (item!=""):
                name2first = unicode(item.lower(),"utf-8",errors="ignore")
        if name2lens>3: continue 
        if isSame(name1first,name2first) and isSame(name1last,name2last):
            candidate[tname] = dicIn[oname][tname]
    if (len(candidate)>1) or (len(candidate)==0): continue
    dicHindex[oname] = {}
    dicHindex[oname][tname] = dicIn[oname][tname]

print "Begin Writing"

for oname in dicHindex:
    for tname in dicHindex[oname]:
        st = str(oname) + "\t" + str(tname) + "\t" + str(dicHindex[oname][tname]) + "\n"
        fout.write(st)

pickle.dump(dicHindex,foutdump)
