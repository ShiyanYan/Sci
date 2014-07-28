#AuthorListGenrate.py
#Parse Metadata
#to parse xml file into field data
import glob
import cPickle as pickle
from bs4 import BeautifulSoup

authorlist = []
fileNames = glob.glob('../../../ACMdata/proceeding/*.xml')

cc = 0
output = open("../../ACMdata/ID_Metadata_Proc.txt","wb")
for f in fileNames:
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc  += 1 
    if cc % 100==0: print "Proc" +str(cc) + " Complete"
    if cc>10: break
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").text
        output.write("ID "+ Id + "\n") # parsing ID
        
        Aus =  ar.findAll('au') 
        aus = []
        for au in Aus:
            if au.find('person_id'):
                aus.append([au.find('last_name').text + ', ' + au.find('first_name').text, au.find('person_id').text])

        if len(Aus) > 1:
            output.write('AU ' + Aus[0].find('first_name').text + ' ' + Aus[0].find('middle_name').text + ' ' + Aus[0].find('last_name').text + '\n')
            for au in Aus[1:]:
                output.write(' ' + au.find('first_name').text + ' ' + au.find('middle_name').text + ' ' + au.find('last_name').text + '\n')
        else:
            if (len(Aus)>=1):
                output.write('AU ' + Aus[0].find('first_name').text + ' ' + Aus[0].find('middle_name').text + ' ' + Aus[0].find('last_name').text + '\n')
        for au in Aus:
            if au.find('affiliation'):
                output.write('AF ' + au.find('affiliation').text + '\n')

output.close()

