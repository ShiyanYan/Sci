#Parse Metadata
#to parse xml file into field data
import glob
import cPickle as pickle
from bs4 import BeautifulSoup

authorlist = []
fileNames = glob.glob('../../../ACMdata/periodical/*.xml')

cc = 0
output = open("../../ACMdata/ID_Metadata2.txt","wb")
for f in fileNames:
    xml = open(f, 'rU').read()
    soup = BeautifulSoup(xml)
    cc  += 1 
    print "Proc" +str(cc) + " Complete"
#    if cc>10: break
    for ar in soup.findAll('article_rec'):
        Id = ar.find("article_id").text
        output.write("ID "+ Id + "\n") # parsing ID
        if ar.find("title")!=None:
            ti = ar.find("title").text
        else:
            ti = ""
        if (ar.find("subtitle")!=None):
            subti = ar.find("subtitle").text
        else:
            subti = ""
        tt = ti
        if subti!="": tt = ti+": "+subti # parsing TI
        output.write("TI " + tt.encode("UTF-8") + "\n")
        output.write('CI 0' + '\n') # Writing CI
        if soup.find('series_title'):
            output.write('SO ' + soup.find('series_title').text + '\n')
        else:
            if soup.find("proc_title"):
                output.write('SO ' + soup.find('proc_title').text + '\n')
        # parsing SO
        
        #if ar.find('page_from') and ar.find('page_to') and (ar.find("article_publication_date")!=None)  and (soup.find('proc_desc')!=None):
        #    output.write('BI ' + soup.find('proc_desc').text + ': ' + ar.find('page_from').text + '-' + ar.find('page_to').text + ' ' + ar.find('article_publication_date').text + '\n')
        #else:
        #    output.write('BI ' + soup.find('proc_desc').text + ': ' + ar.find('article_publication_date').text + '\n')    
  
       # parsing BI
        Aus =  ar.findAll('au') 
        aus = []
        for au in Aus:
            if au.find('person_id'):
                aus.append([au.find('last_name').text + ', ' + au.find('first_name').text, au.find('person_id').text])

        if len(Aus) > 1:
            output.write('AU ' + Aus[0].find('last_name').text + ', ' + Aus[0].find('first_name').text + '\n')
            for au in Aus[1:]:
                output.write(' ' + au.find('last_name').text + ', ' + au.find('first_name').text + '\n')
        else:
            if (len(Aus)>=1):
                output.write('AU ' + Aus[0].find('last_name').text + ', ' + Aus[0].find('first_name').text + '\n')
        for au in Aus:
            if au.find('affiliation'):
                output.write('AF ' + au.find('affiliation').text + '\n')
        Ref = ar.findAll('ref')
        for ref in Ref:
            if ref.find('ref_obj_id'):
                output.write('RF ' + ref.find('ref_obj_id').text + '\n')        
        Cat = ar.findAll('cat_node')
        if Cat != '':
            for cat in Cat:
                output.write('CA ' + cat.text + '\n')
        output.write('\n')

output.close()

