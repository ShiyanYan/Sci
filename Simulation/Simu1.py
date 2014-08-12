#Simulation1 contain different parts of simulations in the project
import sys
import math
import cPickle as pickle

IDmatchAuthor = pickle.load(open("../../ACMdata/" + "ID_AU.dump","rb"))
#Get Necessary information
path = "../../ClusterResultsHumanHH2/"

print "Begin Reading Files"
#AuthorMatchTopics = pickle.load(open(path + "AuthorMatchTopics.dump","r"))
PaperNum = pickle.load(open(path + "AuthorPaperNum.dump","r")) # Actually ACP
Examplar = pickle.load(open(path + "exemplar.dump","r"))
CluSimDic = pickle.load(open(path + "CluSimDic","r"))
AuthorList = pickle.load(open("../../ACMdata/HindexAuthorList.dump","r"))
cc = 0
AuthorMatchTopics = {}
IDmatchTopics = pickle.load(open(path + "IdMatchTopics","rb"))
authortot = {}
for Id in IDmatchAuthor:
    cc += 1
    if cc % 100000==0: print str(cc) + " Complete!"
    for au in IDmatchAuthor[Id]:
        if not au in AuthorList: continue
        if not au in AuthorMatchTopics: AuthorMatchTopics[au] = {}
        if not au in authortot: authortot[au] = 1
        else: authortot[au] += 1
        for tot in IDmatchTopics[Id]:
            if tot in AuthorMatchTopics[au]:
                AuthorMatchTopics[au][tot] += IDmatchTopics[Id][tot]
            else:
                AuthorMatchTopics[au][tot] = IDmatchTopics[Id][tot]

for au in AuthorMatchTopics:
    for tot in AuthorMatchTopics[au]:
        AuthorMatchTopics[au][tot] = AuthorMatchTopics[au][tot] / float(authortot[au])


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

alpha = -1
beta = 2

for au in AuthorMatchTopics:
    if not au in AuthorList: continue
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


for au in AuthorMatchTopics:
    if not au in AuthorList: continue
    PaperN = PaperNum[au]
    OldTopics = AuthorMatchTopics[au]
    Topics = {}
    j = 0
    for tot in sorted(OldTopics,key=OldTopics.get,reverse=True):
        j += 1
        if j>1:
            Topics[tot] = float(OldTopics[tot]) * float(PaperN) / float(PaperN + 1) 
        else:
            Topics[tot] = float(OldTopics[tot]) * float(PaperN) / float(PaperN + 1) + float(1) / float(PaperN + 1)
    
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
    if not au in AuthorList: continue
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

print "The Results of Simulation I"

entropyPro = 0
entropy2Pro = 0
SimpPro = 0
GiniPro = 0
GLscorePro = 0
Shiyan1Pro = 0
AN = 0
for au in AuthorMatchTopics:
    if not au in AuthorList: continue
    if entropyOld[au]>=entropyNew[au]: entropyPro += 1
    if entropy2Old[au]>=entropyNew[au]: entropy2Pro += 1
    if SimpOld[au]>=SimpNew[au]: SimpPro += 1
    if GiniOld[au]>=GiniNew[au]: GiniPro += 1
    if GLscoreOld[au]>=GLscoreNew[au]: GLscorePro += 1
    if Shiyan1Old[au]>=Shiyan1New[au]: Shiyan1Pro += 1
    AN += 1

#AN = len(AuthorMatchTopics)

entropyPro = float(entropyPro) / float(AN)
entropy2Pro = float(entropy2Pro) / float(AN)
SimpPro = float(SimpPro) / float(AN)
GiniPro = float(GiniPro) / float(AN)
GLscorePro = float(GLscorePro) / float(AN)
Shiyan1Pro = float(Shiyan1Pro) / float(AN)

print "entropyPro = ",entropyPro
print "entropy2Pro = ",entropy2Pro
print "SimpPro = ",SimpPro
print "GiniPro = ",GiniPro
print "GLscorePro = ",GLscorePro
print "Shiyan1Pro = ",Shiyan1Pro

print AN
