# the second version of simulation codes, a combination of the three different simulation procedures
import sys
import cPickle as pickle
import math
import random

path = "../../ACMdata/"

Authorlist = pickle.load(open(path + "HindexAuthorList.dump","rb"))


path = "../../ClusterResultsHumanHH2/"
AuMatchIDmatchTopics = pickle.load(open(path+"AuMatchIDmatchTopics.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","r"))
PaperNum = pickle.load(open(path + "AuthorPaperNum.dump","r"))
Cohe = pickle.load(open(path + "SimInsideCoauthor.dump","r"))
CluSimDic = pickle.load(open(path + "CluSimDic","r"))
ClosestArea = pickle.load(open(path + "ClosestArea.dump","r"))

def newAreaGenerate(AreaAlready):
    tt = len(exemplar)
    while True:
        newin = random.randint(0,tt-1)
        newex = exemplar[newin]
        if not newex in AreaAlready:
            return newex


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
        return newAreaGenerate(AreaAlready) #changed


def MetriCal(Topics,alpha,beta,gamma):
    j = 0
    scorelist = {}
    topiclist = {}
    for tot in sorted(Topics,key=Topics.get,reverse=True):
        j += 1
        topiclist[j] = tot
        scorelist[j] = Topics[tot]
    scope = j

    Shiyan2score = 0
    for i in range(1,scope+1):
        for j in range(i+1,scope+1):
            if not topiclist[i] in CluSimDic: continue
            if not topiclist[j] in CluSimDic[topiclist[i]]: continue
            si = CluSimDic[topiclist[i]][topiclist[j]]
            if (topiclist[i] in Cohe) and (topiclist[j] in Cohe): Shiyan2score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta) * math.pow( Cohe[topiclist[i]]*Cohe[topiclist[j]],gamma)
    return Shiyan2score

cc = 0

totN = 0

S1S = 0
S2S = 0
S3S = 0

output = open(path + "Simulation_PS_Results_S.csv","wb")
output.write("Alpha,Beta,Gamma,Simu1,Simu2,Simu3,Simu4\n")
for alpha in range(-5,6):
    for beta in range(-5,6):
        for gamma in range(-5,6):
            print "Alpha = ",alpha
            print "Beta = ",beta
            print "Gamma = ",gamma
            cc = 0
            totN = 0
            S1S = 0
            S2S = 0 
            S3S = 0
            S4S = 0
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
                for tot in Topics:
                    Topics[tot] = float(Topics[tot]) / float(ACP)
                if len(Topics)<1: continue
                scores0 = MetriCal(Topics,alpha,beta,gamma)
    
                Topics2 = dict(Topics)
                j = 0
                for tot in sorted(Topics2,key=Topics2.get,reverse=True):
                    j += 1
                    if j>1: 
                        Topics2[tot] = Topics2[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
                    else:
                        Topics2[tot] = Topics2[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1) + float(1) / float(PaperNum[au] + 1)
                scores1 = MetriCal(Topics2,alpha,beta,gamma)
    
                Topics3 = dict(Topics)
                for tot in Topics3:
                    Topics3[tot] = Topics3[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
                T = newAreaGenerate(Topics3)
                Topics3[T] = float(1) / float(PaperNum[au] + 1)
                scores2 = MetriCal(Topics3,alpha,beta,gamma)
    
                Topics4 = dict(Topics3)
                for tot in Topics4:
                    Topics4[tot] = Topics4[tot] * float(PaperNum[au] + 1) / float(PaperNum[au] + 2)
                T = newAreaGenerate(Topics4)
                Topics4[T] = float(1) / float(PaperNum[au] + 2)
                scores3 = MetriCal(Topics4,alpha,beta,gamma)
                
                Topics5 = dict(Topics)
                for tot in Topics5:
                    Topics5[tot] = Topics5[tot] * float(PaperNum[au]) / float(PaperNum[au] + 1)
                T = closestAreaGenerate(Topics5)
                Topics5[T] = float(1) / float(PaperNum[au] + 1)
                scores4 = MetriCal(Topics5,alpha,beta,gamma)

                totN += 1
                if scores1<scores0: S1S += 1
                if scores2>scores0: S2S += 1
                if (scores2>scores0) and (scores3>scores2) and (scores3-scores2<scores2-scores0): S3S += 1
                if scores4<scores2: S4S += 1
            

            print "The Results" + " is:"
            print "Simu1: " + str(float(S1S) / float(totN)) + " Simu2: " + str(float(S2S)/float(totN)) + " Simu3: " + str(float(S3S)/float(S2S)) + " Simu4: " + str(float(S4S)/float(totN))
            output.write(str(alpha) + "," + str(beta) + "," + str(gamma) + "," + str(float(S1S)/float(totN)) + "," + str(float(S2S)/float(totN)) + "," + str(float(S3S)/float(S2S)) + "," + str(float(S4S)/float(totN)) + "\n")

output.close()
