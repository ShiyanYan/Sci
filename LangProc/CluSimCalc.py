#CluSimCalc.py the program to calculate similarity between clusters  the old version in ClusterSim.py is not useful now
import cPickle as pickle
import sys
path = "../../ClusterResultsHumanES4/"
DicForClu = pickle.load(open(path + "DicForClu.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","rb"))
dic = pickle.load(open(path + "dic","rb"))
sim = open(path + "similarity","rb")

outfile = open(path + "clusterSim","w") # output file should be an adjecent table
numOfLinks = {}
sumOfSim = {}

for line in sim:
    ss = line.split("\t")
    n1 = int(ss[0])
    n2 = int(ss[1])
    simValue = float(ss[2][0:len(ss[2])-1])
    w1 = dic[n1]
    w2 = dic[n2]
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

for tt in numOfLinks:
    clu1 = tt / 1000
    clu2 = tt % 1000
    ex1 = exemplar[clu1]
    ex2 = exemplar[cllu2]
    si = float(sumOfSim[index]) / numOfLinks[index]
    outfile.write( ex1 + "\t" + ex2 + "\t" + str(si) + "\n")  