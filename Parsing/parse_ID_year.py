#parse_ID_reference.py
# store the ID:reference dict in the dump
import glob
import sys
from bs4 import BeautifulSoup
import cPickle as pickle 

fileNames = glob.glob('../../../ACMdata/proceeding/*.xml')
output = open("../../ACMdata/ID_Year.dump","w")
ID_YR = {}
cc = 0
for f in fileNames:
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc += 1
#    if cc>1: break 
    if cc % 100 ==0: print "Proc" +str(cc) + " Complete"
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").text
        if len(Id)<1: continue
        year = "0"
        if ar.find('article_publication_date'):
            year = ar.find('article_publication_date').text[-4:]
        if len(year)==4:
            ID_YR[Id] = int(year)
#           if cc <=10: print ID_YR[Id]
pickle.dump(ID_YR,output)                        

output.close()
