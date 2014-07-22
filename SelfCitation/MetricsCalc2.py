#MetricsCalc2.py
import cPickle as pickle
import sys

path = sys.argv[1]

subpapers = pickle.load(open(path+"subpapers.dump"),"r")
IdMatchTopics = pickle.load(open(path + "IdMatchTopics","r"))
CluSimDic = pickle.load(open(path + "CluSimDic"),"r")

subsubpapersID = []
for au in AL:
    for p in subpapers:
        if au in p.AU:
            subsubpapersID.append(p.ID)
    tot = {}
    paparN = 0
    for ID in subsubpapersID：
        paperN +=1
        ss = IdMatchTopics[ID]
        for topic in ss:
            if topic in tot:
                tot[topic] += ss[topic]
            else:
                tot[topic] = ss[topic]
    for topic in tot:
        tot[topic] = tot[topic] / paperN
    print "The author " + str(au) + " have published " +str(paperN) + " papers in ACM.\n"
    j = 0
    for topic in sorted(tot,key=tot,get,reverse=True):
        j += 1
        print str(j),topic,str(tot[topic])
    

    
