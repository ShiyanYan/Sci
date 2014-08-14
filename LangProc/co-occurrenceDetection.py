#co-occurrence detection
dicLink = {}
import collections
import cPickle as pickle
import sys
dic = []
TT = 0
infile = open(sys.argv[1],"r")
for line in infile:
    TT += 1
    if (TT % 10000==0): print "Complete " + str(TT)
    if len(line)==0: continue
    line = line[0:len(line)-1]
    ss = line.split("\t")
    # print ss
    leng = len(ss)
    # print leng
    for i in range(0,leng-1):
        for j in range(i+1,leng):
            if (ss[i]=="") or (ss[j]==""): continue
            s = ss[i] + "\t" + ss[j]
            if not (ss[i] in dic): dic.append(ss[i])
            if not (ss[j] in dic): dic.append(ss[j]) 
            if s in dicLink:
                dicLink[s] +=1
            else:
                dicLink[s] = 1

outfile = open(sys.argv[2],"w")
dicLink = collections.OrderedDict(sorted(dicLink.items()))
print len(dicLink)
MAX = 0
for item in dicLink:
    ss = item.split("\t")
    #print dicLink[item
    if dicLink[item]>MAX: MAX = dicLink[item]   #the max value of cooccurence
    outfile.write(ss[0] + "\t" + ss[1] + "\t" + str(dicLink[item]) + "\n")

outfile.close()
print MAX
dic = sorted(dic)
out = open(sys.argv[3],"w")
pickle.dump(dic,out)
out.close()