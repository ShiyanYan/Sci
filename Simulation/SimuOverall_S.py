# the second version of simulation codes, a combination of the three different simulation procedures
import sys
import cPickle as pickle
import math
import random
sys.path.append("../Time-series/")

import metricesCal

path = "../../ACMdata/"

Authorlist = pickle.load(open(path + "HindexAuthorList.dump","rb"))


path = "../../ClusterResultsHumanHH2/"
AuMatchIDmatchTopics = pickle.load(open(path+"AuMatchIDmatchTopics.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","r"))
PaperNum = pickle.load(open(path + "AuthorPaperNum.dump","r"))

Nmetrics = 7
MetricsNames = ["Entropy","Entropy2","Simpson","Gini","GLscore","Shiyan1","Shiyan2"]
def newAreaGenerate(AreaAlready):
    tt = len(exemplar)
    while True:
        newin = random.randint(0,tt-1)
        newex = exemplar[newin]
        if not newex in AreaAlready:
            return newex

cc = 0

totN = 0

S1S = []
S2S = []
S3S = []

for i in range(0,Nmetrics):
    S1S.append(0)
    S2S.append(0)
    S3S.append(0)

for au in Authorlist:
    if not au in AuMatchIDmatchTopics: continue
    if not au in PaperNum: continue
    cc += 1
    if cc % 1000==0: print str(cc) + " Complete!"
    Topics = {}
    IdmatchTopics = AuMatchIDmatchTopics[au]
    if len(IdmatchTopics)<1: continue
    for Id in IdmatchTopics:
        for tot in IdmatchTopics[Id]:
             if tot in Topics: Topics[tot] += IdmatchTopics[Id][tot]
             else: Topics[tot] = IdmatchTopics[Id][tot]
    for tot in Topics:
        Topics[tot] = float(Topics[tot]) / float(len(IdmatchTopics))
    if len(Topics)<1: continue
    scores0 = metricesCal.MetriCal(Topics)
    
    Topics2 = Topics
    j = 0
    for tot in sorted(Topics2,key=Topics2.get,reverse=True):
        j += 1
        if j>1: 
            Topics2[tot] = Topics2[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
        else:
            Topics2[tot] = Topics2[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1) + float(1) / float(PaperNum[au] + 1)
    scores1 = metricesCal.MetriCal(Topics2)
    
    Topics3 = Topics
    for tot in Topics3:
        Topics3[tot] = Topics3[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
    T = newAreaGenerate(Topics)
    Topics3[T] = float(1) / float(PaperNum[au] + 1)
    
    scores2 = metricesCal.MetriCal(Topics3)
    
    Topics4 = Topics3
    for tot in Topics4:
        Topics4[tot] = Topics4[tot] * float(PaperNum[au] + 1) / float(PaperNum[au] + 2)
    T = newAreaGenerate(Topics3)
    Topics4[T] = float(1) / float(PaperNum[au] + 2)
    scores3 = metricesCal.MetriCal(Topics4)
    
    totN += 1
    for i in range(0,Nmetrics):
        if scores1[i]<scores0[i]: S1S[i] += 1
        if scores2[i]>scores0[i]: S2S[i] += 1
        if (scores2[i]>scores0[i]) and (scores3[i]>scores2[i]) and (scores3[i]-scores2[i]<scores2[i]-scores0[i]): S3S[i] += 1


print "The results of simulation for all the metrices"

output = open(path + "SimulationResults.csv","wb")
output.write("MetricName,Simu1,Simu2,Simu3\n")

for i in range(0,Nmetrics):
    print "The Results of " + MetricsNames[i] + " is"
    print "Simu1: " + str(float(S1S[i]) / float(totN)) + " Simu2: " + str(float(S2S[i])/float(totN)) + " Simu3: " + str(float(S3S[i])/float(S2S[i]))
    output.write(str(float(S1S[i])/float(totN)) + "," + str(float(S2S[i])/float(totN)) + "," + str(float(S3S[i])/float(S2S[i])) + "\n")

output.close()
