#to parse xml file into field data
import glob
import cPickle as pickle
from BeautifulSoup import *

authorlist = []
fileNames = glob.glob('../../ACMdata/proceeding/*.xml')

cc = 0
for f in fileNames:
    ss = f.split("-")
    output = open('../../ACMdata/proceeding/'+ss[1], 'wb')
    output.write(ss[1] + "\n")
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc  += 1 
    print "Proc" +str(cc) + " Complete"
    for ar in soup.findAll('article_rec'):
        ti = ar.find("title").text
        if (ar.find("subtitle")!=None):
            subti = ar.find("subtitle").text
        else:
            subti = ""
        if (ar.find("abstract").find("par")!=None):
            ab = ar.find("abstract").find("par").text
        else:
            if (ar.find("abstract").find("p")!=None):
                ab = ar.find("abstract").find("p")
            else:
                ab = ""
        if ab.find("<p>")>=0:
            ab = ab[3:len(ab)-4]
        tt = ti
        if subti!="": tt = ti+": "+subti
        output.write(tt+"\n")
        output.write(ab+"\n")
    output.write("\n")

output.close()

