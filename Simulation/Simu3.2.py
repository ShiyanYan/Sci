#Simulation2 add a new area experiments
import sys
import math
import cPickle as pickle
import random
#Get Necessary information
path = "../../ClusterResultsHumanHH2/"

print "Begin Reading Files"
AuthorMatchTopics = pickle.load(open(path + "AuthorMatchTopics.dump","r"))
PaperNum = pickle.load(open(path + "AuthorPaperNum.dump","r")) # Actually ACP
exemplar = pickle.load(open(path + "exemplar.dump","r"))
CluSimDic = pickle.load(open(path + "CluSimDic","r"))

AuthorList = pickle.load(open("../../ACMdata/AuthorList_above5.dump","r"))
temp = {}
for au in AuthorMatchTopics:
    if len(AuthorMatchTopics[au])==0: continue
    temp[au] = AuthorMatchTopics[au]

AuthorMatchTopics = temp

print "End Reading Files"

#First, check the results of "Add the Highest"

AuthorMatchTopicsNew = {}

GLscoreOld = {}
entropyOld = {}
entropy2Old = {}
SimpOld = {}
GiniOld = {}  # actually 1 - Gini
Shiyan1Old = {}
print "Begin to calculate the old scores of metrics"

alpha = -0.5
beta = 1

for au in AuthorMatchTopics:
    Topics = AuthorMatchTopics[au]    
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
    for i in range(1,scope+1):
        for j in range(i+1,scope+1):
            if not topiclist[i] in CluSimDic: continue
            if not topiclist[j] in CluSimDic[topiclist[i]]: continue
            si = CluSimDic[topiclist[i]][topiclist[j]]
            GLscore += math.pow(si,alpha) * math.pow(scorelist[i]*scorelist[j],beta)
            Shiyan1score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta)
   

    entropyOld[au] = en
    entropy2Old[au] = en2
    SimpOld[au] = Simp
    GiniOld[au] = float(totq) / float(len(Topics))
    GLscoreOld[au] = GLscore
    Shiyan1Old[au] = Shiyan1score

print "End of calculation of old scores"
print "Begin to generate New assignment for Simulation1"

def newAreaGenerate(AreaAlready):
    tt = len(exemplar)
    while True:
        newin = random.randint(0,tt-1)
        newex = exemplar[newin]
        if not newex in AreaAlready:
            return newex
        
for au in AuthorMatchTopics:
    PaperN = PaperNum[au]
    OldTopics = AuthorMatchTopics[au]
    Topics = {}
    j = 0
    for tot in sorted(OldTopics,key=OldTopics.get,reverse=True):
        j += 1
        Topics[tot] = float(OldTopics[tot]) * float(PaperN) / float(PaperN + 1) 
    T = newAreaGenerate(Topics)
    Topics[T] = float(1) / float(PaperN + 1)
    AuthorMatchTopicsNew[au] = Topics
            
print "End of New assignment"

print "Begin to Calculate New Scores"

GLscoreNew = {}
entropyNew = {}
entropy2New = {}
SimpNew = {}
GiniNew = {}  # actually 1 - Gini
Shiyan1New = {}

for au in AuthorMatchTopicsNew:
    Topics = AuthorMatchTopicsNew[au]
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
    for i in range(1,scope+1):
        for j in range(i+1,scope+1):
            if not topiclist[i] in CluSimDic: continue
            if not topiclist[j] in CluSimDic[topiclist[i]]: continue
            si = CluSimDic[topiclist[i]][topiclist[j]]
            GLscore += math.pow(si,alpha) * math.pow(scorelist[i]*scorelist[j],beta)
            Shiyan1score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta)


    entropyNew[au] = en
    entropy2New[au] = en2
    SimpNew[au] = Simp
    GiniNew[au] = float(totq) / float(len(Topics))
    GLscoreNew[au] = GLscore
    Shiyan1New[au] = Shiyan1score

print "End of Calculation of new scores"

print "Begin of New Assignment Stage II"

AuthorMatchTopicsNew2 = {}

for au in AuthorMatchTopicsNew:
    PaperN = PaperNum[au]
    OldTopics = AuthorMatchTopicsNew[au]
    Topics = {}
    j = 0
    for tot in sorted(OldTopics,key=OldTopics.get,reverse=True):
        j += 1
        Topics[tot] = float(OldTopics[tot]) * float(PaperN + 1) / float(PaperN + 2) 
    T = newAreaGenerate(Topics)
    Topics[T] = float(1) / float(PaperN + 2)
    AuthorMatchTopicsNew2[au] = Topics
            
print "End of New assignment Stage II"

print "Begin to Calculate New Scores"

GLscoreNew2 = {}
entropyNew2 = {}
entropy2New2 = {}
SimpNew2 = {}
GiniNew2 = {}  # actually 1 - Gini
Shiyan1New2 = {}

for au in AuthorMatchTopicsNew2:
    Topics = AuthorMatchTopicsNew2[au]
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
    for i in range(1,scope+1):
        for j in range(i+1,scope+1):
            if not topiclist[i] in CluSimDic: continue
            if not topiclist[j] in CluSimDic[topiclist[i]]: continue
            si = CluSimDic[topiclist[i]][topiclist[j]]
            GLscore += math.pow(si,alpha) * math.pow(scorelist[i]*scorelist[j],beta)
            Shiyan1score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta)


    entropyNew2[au] = en
    entropy2New2[au] = en2
    SimpNew2[au] = Simp
    GiniNew2[au] = float(totq) / float(len(Topics))
    GLscoreNew2[au] = GLscore
    Shiyan1New2[au] = Shiyan1score

print "The Results of Simulation III.II"

entropyPro = 0
entropyTot = 0
entropy2Pro = 0
entropy2Tot = 0
SimpPro = 0
SimpTot = 0
GiniPro = 0
GiniTot = 0
GLscorePro = 0
GLscoreTot = 0
Shiyan1Pro = 0
Shiyan1Tot = 0

for au in AuthorMatchTopics:
    if entropyOld[au]<=entropyNew[au]:
        entropyTot += 1
        if (entropyNew[au]>entropyNew2[au]):  # Marginally decrease
            entropyPro += 1
    if entropy2Old[au]<=entropyNew[au]: 
        entropy2Tot += 1
        if (entropy2New[au]>entropy2New2[au]): #Marginally decrease
            entropy2Pro += 1
    if SimpOld[au]<=SimpNew[au]: 
        SimpTot += 1
        if (SimpNew[au]>SimpNew2[au]): # Marginally decrease
            SimpPro += 1
    if GiniOld[au]<=GiniNew[au]:
        GiniTot += 1
        if (GiniNew[au]>GiniNew2[au]): # Marginally decrease
            GiniPro += 1
    if GLscoreOld[au]<=GLscoreNew[au]: 
        GLscoreTot += 1
        if (GLscoreNew[au]>GLscoreNew2[au]): # Marginally decrease
            GLscorePro += 1
    if Shiyan1Old[au]<=Shiyan1New[au]: 
        Shiyan1Tot += 1
        if (Shiyan1New[au]>Shiyan1New2[au]): # Marignally decrease 
            Shiyan1Pro += 1

AN = len(AuthorMatchTopics)

entropyPro = float(entropyPro) / float(entropyTot)
entropy2Pro = float(entropy2Pro) / float(entropy2Tot)
SimpPro = float(SimpPro) / float(SimpTot)
GiniPro = float(GiniPro) / float(GiniTot)
GLscorePro = float(GLscorePro) / float(GLscoreTot)
Shiyan1Pro = float(Shiyan1Pro) / float(Shiyan1Tot)

print "entropyPro = ",entropyPro
print "entropy2Pro = ",entropy2Pro
print "SimpPro = ",SimpPro
print "GiniPro = ",GiniPro
print "GLscorePro = ",GLscorePro
print "Shiyan1Pro = ",Shiyan1Pro


