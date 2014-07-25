#SimInsidedCluster.py to calculate the similarity inside a cluster
import cPickle as pickle
import sys
import math
path = sys.argv[1]
DicForClu = pickle.load(open(path + "DicForClu.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","rb"))
dic = pickle.load(open(path + "dict","rb"))
sim = open(path + "similarityFile","rb")
output = open(path + "SimInside","wb")

numOfLinks = {}
sumOfSim = {}

avInSim = {}

print "Length of WordDic=", len(dic)
tt = 0
for line in sim:
    tt += 1
#    if tt>10: break
    ss = line.split("\t")
    n1 = int(ss[0])
    n2 = int(ss[1])
    simValue = float(ss[2][0:len(ss[2])-1])
    w1 = dic[n1-1]
    w2 = dic[n2-1]
    if not w1 in DicForClu: continue
    if not w2 in DicForClu: continue
    clu1 = DicForClu[w1]
    clu2 = DicForClu[w2]
    if clu1!=clu2: continue
    ex1 = exemplar[clu1]
    numOfLinks[ex1] += 1
    sumOfSim[ex1] += simValue

for ex in numOfLinks: 
    avsim = float(sumOfSim) / float(numOfLinks)
    avInSim[ex] = avsim
    print ex,avsim

pickle.dump(avInSim,output)

    

