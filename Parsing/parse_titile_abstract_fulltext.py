#to parse xml file into field data
import glob
import cPickle as pickle
from BeautifulSoup import *

authorlist = []
fileNames = glob.glob('../../../ACMdata/proceeding/*.xml')

cc = 0
output = open("../../ACMdata/ID_AB_FT.txt","wb")
for f in fileNames:
    ss = f.split("-")
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc  +=1 
    print "Proc" +str(cc) + " Complete"
    if cc>10: break
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").txt
        output.write("ID "+ Id + "\n")
        ti = ar.find("title").text
        if (ar.find("subtitle")!=None):
            subti = ar.find("subtitle").text
        else:
            subti = ""
        if (ar.find("abstract").find("par")!=None):
            ab = ar.find("abstract").find("par").text
        else:
            if (ar.find("abstract").find("p")!=None):
                ab = ar.find("abstract").find("p").text
            else:
                ab = ar.find("abstract").text
        if ab.find("<p>")>=0:
            ab = ab[3:len(ab)-4]
        tt = ti
        if subti!="": tt = ti+": "+subti
        output.write("TI " + tt + "\n")
        output.write("AB \n")
        output.write(ab+"\n")
        if (ar.find("ft_body")!=None):
            Ft = ar.find("ft_body").text
        output.write("FT \n")
        output.write(Ft + "\n")
output.close()

