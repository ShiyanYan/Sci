#parse_ID_reference.py
# store the ID:reference dict in the dump
import sys
from bs4 import BeautifulSoup
import cPickle as pickle 

fileNames = glob.glob('../../../ACMdata/proceeding/*.xml')
output = open("../../ACMdata/ID_RF.dump","w")
ID_RF = {}
for f in fileNames
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc  += 1 
    if cc>10: break
    if cc % 100 ==0: print "Proc" +str(cc) + " Complete"
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").text
        if len(Id)<1: continue
        ID_RF[Id] = []
        print Id
        Ref = ar.findAll('ref')
        for ref in Ref:
            if ref.find('ref_obj_id'):
                ID_RF[Id].append(ref.find('ref_obj_id').text)
        print ID_RF[Id]

pickle.dump(ID_RF,output)                        

output.close()