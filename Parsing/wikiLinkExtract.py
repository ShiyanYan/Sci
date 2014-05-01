#wikiLinkExtract.py
infile = open("../../Wiki/Category/firstline.txt","rb")
outfile = open("../../Wiki/Category/test","wb")
tt = 0
for line in infile:
    if line[0:6]!="INSERT": continue
    tuplist = line.split("),(")
    # process tuple 1  INSERT INTO `categorylinks` VALUES (0,'','','2014-01-16 15:23:19','','','page'
    # process tuple other 10,'Redirects_with_old_history','ACCESSIBLECOMPUTING','2010-08-26 22:38:36','','uppercase','page'
    # may be , and '  in the text
    for tup in tuplist:
        ele = tup.split(",'")
        tt +=1
        sfrom = ele[1][0:len(ele[1])-1]
        sto = ele[2][0:len(ele[2])-1]
        if sfrom == "": continue
        if sto == "": continue
        sfrom = sfrom.lower()
        sfrom = sfrom.replace("_"," ")
        sto = sto.lower()
        sto = sto.replace("_"," ")
        if (tt>53) and (tt<55): print sto
        stoss = sto.split("\\n")
        if (tt>53) and (tt<55): print stoss
        for term in stoss:
            if len(term)<=1: continue
            outfile.write(sfrom+"\t"+term+"\n")
    break    