# The sub codes to compute the metrices for every assignment
# This code will be imported by many other codes to calculate the scores of metrics
import sys
import math
import cPickle as pickle

path = "../../ClusterResultsHumanHH2/"
Examplar = pickle.load(open(path + "exemplar.dump","r"))
CluSimDic = pickle.load(open(path + "CluSimDic","r"))
Cohe = pickle.load(open(path + "SimInsideCoauthor.dump","r"))
MetricsNum = 7  # The number of metrics
alpha = -5
beta = 1
gamma = -1
print "Alpha = ",alpha
print "Beta = ",beta
print "Gamma = ",gamma
def MetriCal(Topics):
    results = []
    for i in range(0,MetricsNum):
        results.append(0)
    en = 0
    en2 = 0
    Simp = 1
    q1 = 0
    q2 = 0
    totq = 0
    j = 0
    scorelist = {}
    topiclist = {}
    for tot in sorted(Topics,key=Topics.get,reverse=True):
        j += 1
        topiclist[j] = tot
        scorelist[j] = Topics[tot]
        if Topics[tot]<=0: continue
        if len(Topics)<=1: continue
        en -= float(Topics[tot]) * math.log(Topics[tot],len(Topics))
        en2 -= float(Topics[tot]) * math.log(Topics[tot],2)
        Simp -= Topics[tot] * Topics[tot]

    for tot in sorted(Topics,key=Topics.get,reverse=False):
        q2 = q1 + Topics[tot]
        totq = totq + q1 +q2
        q1 = q2

    scope = j
    GLscore = 0
    Shiyan1score = 0
    Shiyan2score = 0
    for i in range(1,scope+1):
        for j in range(i+1,scope+1):
            if not topiclist[i] in CluSimDic: continue
            if not topiclist[j] in CluSimDic[topiclist[i]]: continue
            si = CluSimDic[topiclist[i]][topiclist[j]]
            GLscore += math.pow(si,alpha) * math.pow(scorelist[i]*scorelist[j],beta)
            Shiyan1score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta)
            if (topiclist[i] in Cohe) and (topiclist[j] in Cohe): Shiyan2score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta) * math.pow(1 / (Cohe[topiclist[i]]*Cohe[topiclist[j]]),gamma)
    results[0] = en # entropy
    results[1] = en2 # entropy2
    results[2] = Simp # simpson
    results[3] = float(totq) / float(len(Topics)) # 1 - Gini Index
    results[4] = GLscore # Generalized Stirling
    results[5] = Shiyan1score # Shiyan1
    results[6] = Shiyan2score # Shiyan2
    return results
