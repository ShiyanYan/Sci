#ClusterExtraction
import cPickle as pickle
infile = open("../../ACMdata/output/apResults","rb")
outfile1 = open("../../ACMdata/DicForClu","wb")
outfile2 = open("../../ACMdata/exemplar","wb")
i = 0
cnum = 0
dic = {}
exemp = {}
for line in infile:
    x = line.find("exemplar")
    if x<0: 
        ss = line.split(" ")
        t = 0
        for item in ss:
            t +=1
            if t==len(ss):
                item = item[0:len(item)-1]
            if item!="":
                dic[item] = cnum
    else:
        be = x + 9
        ed = line.find(":")
        ex = line[be:ed]
        print ex
        cnum += 1
        exemp[cnum] = ex

print len(dic)
i = 0
for item in dic:
    i += 1
    print item,dic[item]
    if i>30: break
pickle.dump(exemp,outfile2)
pickle.dump(dic,outfile1)