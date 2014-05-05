#to parse xml file into field data
import glob
import cPickle as pickle
from bs4 import BeautifulSoup

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
#    if cc>10: break
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").text
        output.write("ID "+ Id + "\n")
        if ar.find("title")!=None:
            ti = ar.find("title").text
        else:
            ti = ""
        if (ar.find("subtitle")!=None):
            subti = ar.find("subtitle").text
        else:
            subti = ""
        ab = ""
        if (ar.find("abstract")!=None):
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
        output.write("TI " + tt.encode("UTF-8") + "\n")
        output.write("AB \n")
        output.write(ab.encode("UTF-8")+"\n")
        if (ar.find("ft_body")!=None):
            Ft = ar.find("ft_body").text
        output.write("FT ")
        output.write(Ft.encode("UTF-8") + "\n")
output.close()

