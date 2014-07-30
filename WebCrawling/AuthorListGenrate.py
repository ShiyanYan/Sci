#AuthorListGenrate.py
#Parse Metadata
#to parse xml file into field data
import glob
import cPickle as pickle
from bs4 import BeautifulSoup

authorlist = []
fileNames = glob.glob('../../../ACMdata/proceeding/*.xml')
IDmatchName = {}
cc = 0
allauthor = []
outdump = open("../../ACMdata/ID_AU.dump","wb")
output = open("../../ACMdata/ID_AU_AF","wb")
for f in fileNames:
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc  += 1 
    if cc % 100==0: print "Proc" +str(cc) + " Complete"
#    if cc>10: break
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").text
        IDmatchName[Id] = []
        output.write("ID "+ Id + "\n") # parsing ID
        
        Aus =  ar.findAll('au') 
        if len(Aus) > 1:
            ss = Aus[0].find('first_name').text + ' ' + Aus[0].find('middle_name').text + ' ' + Aus[0].find('last_name').text
            IDmatchName[Id].append(ss)
            output.write('AU ' + ss + '\n')
            allauthor.append(ss)
            for au in Aus[1:]:
                ss =  au.find('first_name').text + ' ' + au.find('middle_name').text + ' ' + au.find('last_name').text
                output.write(' ' + ss + '\n')
                IDmatchName[Id].append(ss)
                allauthor.append(ss)
        else:
            if (len(Aus)>=1):
                ss = Aus[0].find('first_name').text + ' ' + Aus[0].find('middle_name').text + ' ' + Aus[0].find('last_name').text
                IDmatchName[Id].append(ss)
                allauthor.append(ss)
                output.write('AU ' + ss + '\n')
        for au in Aus:
            if au.find('affiliation'):
                output.write('AF ' + au.find('affiliation').text + '\n')
pickle.dump(IDmatchName,outdump)

output.close()
print "Total Number of Authors=",len(allauthor)
allauthor = sorted(allauthor)
allauthor2 = {}
lastterm = ""
for au in allauthor:
    if au==lastterm:
        allauthor2[au] += 1
        continue
    allauthor2[au] = 1
    lastterm = au

outAlldump = open("../../ACMdata/AuthorList_all.dump","wb")
pickle.dump(allauthor2,outAlldump)
print "TotalNum=",len(allauthor2)
