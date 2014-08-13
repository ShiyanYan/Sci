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
CluSimDic = pickle.load(open(path + "CluSimDic","r"))
ClosestArea = pickle.load(open(path + "ClosestArea.dump","r"))
Nmetrics = 7
MetricsNames = ["Entropy","Entropy2","Simpson","Gini","GLscore","Shiyan1","Shiyan2"]

def newAreaGenerate(AreaAlready):
    tt = len(exemplar)
    j = 0
#    print AreaAlready
    newex = ""
    while True:
        newin = random.randint(0,tt-1)
        newex = exemplar[newin]
        if (not (newex in AreaAlready)):
            j += 1
            return newex
            break           
#    print newex
#    return newex

def closestAreaGenerate(AreaAlready):
    HstSim = 0
    ClsArea = ""
    for tot in AreaAlready:
        if not tot in CluSimDic: continue
        a1 = dict(ClosestArea[tot])
        for nt in a1:
            if nt in AreaAlready: continue
            if ClosestArea[tot][nt]>HstSim:
                HstSim = ClosestArea[tot][nt]
                ClsArea = nt
    if ClsArea!="": 
        return ClsArea
    else:
        print "!!" 
        return newAreaGenerate(AreaAlready) #changed


cc = 0

totN = 0

S1S = []
S2S = []
S3S = []
S4S = []
for i in range(0,Nmetrics):
    S1S.append(0)
    S2S.append(0)
    S3S.append(0)
    S4S.append(0)
T = ""
Topics = {}
Topics2 ={}
Topics3 ={}
Topics4 ={}
Topics5 ={}
for au in Authorlist:
    if not au in AuMatchIDmatchTopics: continue
    if not au in PaperNum: continue
    cc += 1
    if cc % 1000==0: print str(cc) + " Complete!"
    Topics = {}
    IdmatchTopics = dict(AuMatchIDmatchTopics[au])
    if len(IdmatchTopics)<1: continue
    ACP = 0
    for Id in IdmatchTopics:
        if len(IdmatchTopics[Id])>0: ACP += 1
        for tot in IdmatchTopics[Id]:
             if tot in Topics: Topics[tot] += IdmatchTopics[Id][tot]
             else: Topics[tot] = IdmatchTopics[Id][tot]
    sumt = 0
    for tot in Topics:
        Topics[tot] = float(Topics[tot]) / float(ACP)
        sumt += Topics[tot]
    if len(Topics)<1: continue
    scores0 = metricesCal.MetriCal(Topics)
    Topics2 = {}
    Topics2 = dict(Topics)
    j = 0
    for tot in sorted(Topics2,key=Topics2.get,reverse=True):
        j += 1
        if j>1: 
            Topics2[tot] = Topics2[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
        else:
            Topics2[tot] = Topics2[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1) + float(1) / float(PaperNum[au] + 1)
    scores1 = metricesCal.MetriCal(Topics2)

    Topics3 = dict(Topics)
    for tot in Topics3:
        Topics3[tot] = Topics3[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
    T = newAreaGenerate(Topics3)
    if T in Topics: print "ERROR"
    Topics3[T] = float(1) / float(PaperNum[au] + 1)
    scores2 = metricesCal.MetriCal(Topics3)

    Topics4 = dict(Topics3)
    for tot in Topics4:
        Topics4[tot] = Topics4[tot] * float(PaperNum[au] + 1) / float(PaperNum[au] + 2)
    T = newAreaGenerate(Topics4)
    Topics4[T] = float(1) / float(PaperNum[au] + 2)
    scores3 = metricesCal.MetriCal(Topics4)

    Topics5 = dict(Topics)
 #   print Topics5
    for tot in Topics5:
        Topics5[tot] = Topics5[tot] * float(PaperNum[au]) / float( PaperNum[au] +1 )    
    T = closestAreaGenerate(Topics5)
    if T in Topics5: print "ERROR"
    Topics5[T] = float(1) / float(PaperNum[au] +1)
    scores4 = metricesCal.MetriCal(Topics5)
    totN += 1
    for i in range(0,Nmetrics):
        if scores1[i]<scores0[i]: S1S[i] += 1
        if scores2[i]>scores0[i]: S2S[i] += 1
        if (scores2[i]>scores0[i]) and (scores3[i]>scores2[i]) and (scores3[i]-scores2[i]<scores2[i]-scores0[i]): S3S[i] += 1
        if scores4[i]>scores0[i]: S4S[i] += 1

print "The results of simulation for all the metrics"

output = open(path + "SimulationResults_S.csv","wb")
output.write("MetricName,Simu1,Simu2,Simu3,Simu4\n")

for i in range(0,Nmetrics):
    print "The Results of " + MetricsNames[i] + " is"
    print "Simu1: " + str(float(S1S[i]) / float(totN)) + " Simu2: " + str(float(S2S[i])/float(totN)) + " Simu3: " + str(float(S3S[i])/float(S2S[i])) + " Simu4: " + str(float(S4S[i])/float(totN))
    output.write(str(float(S1S[i])/float(totN)) + "," + str(float(S2S[i])/float(totN)) + "," + str(float(S3S[i])/float(S2S[i])) + "," + str(float(S4S[i])/ float(totN))  + "\n")

output.close()
