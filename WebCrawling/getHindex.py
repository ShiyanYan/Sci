#the codes to crawl Hindex (and other 6 metrics score from google scholar

import sys
import cPickle as pickle
import urllib2
import time
import re

urlprefix = "http://scholar.google.com/citations?user="

reg = re.compile(r'cit-data">(\d+)')
def get_impact(url):
	res = urllib2.urlopen(urlprefix + url).read()
	matches = re.findall(reg, res)
	vec = []
	for match in matches:
		vec.append(match)
	return vec

path = "../../ACMdata/"
fin = pickle.load(open( path + "HindexAuthorList.dump", "r") )

fout = open(path + "HindexResults.txt","wb")
foutdump =open(path + "HindexResults.dump","wb")

HindexMatch = {}

vec = []
i = 0
for oname in fin:
    for tname in fin[oname]:
        i += 1
        url = fin[oname][tname]
        vec = get_impact(str(url))
        st = " ".join(vec) + "\n"
        print str(i) + " " + str(tname) + " " + st
        fout.write(st)
        HindexMatch[tname] = vec
        time.sleep(10)
        
pickle.dump(HindexMatch,foutdump)

fout.close()
foutdump.close()

