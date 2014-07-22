#CluSimCalc.py the program to calculate similarity between clusters  the old version in ClusterSim.py is not useful now
import cPickle as pickle
import sys
import math
path = "../../ClusterResultsHumanES4/"
DicForClu = pickle.load(open(path + "DicForClu.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","rb"))
dic = pickle.load(open(path + "dict","rb"))
sim = open(path + "similarityFile","rb")

outfile = open(path + "clusterSim","w") # output file should be an adjecent table
numOfLinks = {}
sumOfSim = {}

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
    index = clu1 *1000 + clu2
    if index in numOfLinks:
        numOfLinks[index] += 1
    else:
        numOfLinks[index] = 1
    if index in sumOfSim:
        sumOfSim[index] += simValue
    else:
        sumOfSim[index] = simValue

CluSim = {}

for tt in sorted(numOfLinks):
    clu1 = tt / 1000
    clu2 = tt % 1000
    ex1 = exemplar[clu1]
    ex2 = exemplar[clu2]
    si = float(sumOfSim[tt]) / math.sqrt(numOfLinks[tt])
    outfile.write( ex1 + "\t" + ex2 + "\t" + str(si) + "\n")
    if ex1 in CluSim:
        CluSim[ex1][ex2] = si
    else:
        CluSim[ex1] = {}
        CluSim[ex1][ex2] = si  

outfile2 = open(path + "CluSimDic","w")
pickle.dump(CluSim,outfile2)