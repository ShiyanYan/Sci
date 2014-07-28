#SimInsidedCluster.py to calculate the similarity inside a cluster
import cPickle as pickle
import sys
import math
path = sys.argv[1]
DicForClu = pickle.load(open(path + "DicForClu.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","rb"))
dic = pickle.load(open(path + "dict","rb"))
sim = open(path + "similarityFile","rb")
output = open(path + "SimInside.dump","wb")

numOfLinks = {}
sumOfSim = {}

avInSim = {}

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
    if ex1 in numOfLinks:
        numOfLinks[ex1] += 1
    else:
        numOfLinks[ex1] = 1
    if ex1 in sumOfSim:
        sumOfSim[ex1] += simValue
    else:
        sumOfSim[ex1] = simValue
outfile = open(path + "simInside.txt","wb")
for ex in sorted(numOfLinks): 
    avsim = float(sumOfSim[ex]) / float(numOfLinks[ex])
    avInSim[ex] = avsim

for ex in sorted(avInSim,key=avInSim.get,reverse=True):
    outfile.write(str(ex) + "\t" + str(avInSim[ex]) + "\n")

pickle.dump(avInSim,output)

    

