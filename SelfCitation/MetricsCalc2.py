#MetricsCalc2.py
import cPickle as pickle
import sys
import math
class Paper:
    #ID    #CI    #SO    #TI    #BI    #AU []    #AF []    #CT []    #CO []    #RF []    #CA []    #YR    #AB
    def __init__(self):
        self.ID = ''
        self.CI = ''
        self.SO = ''
        self.TI = ''
        self.BI = ''
        self.AU = []
        self.AF = []
        self.CT = []
        self.CO = []
        self.RF = []
        self.CA = []
        self.YR = 0 #integer
        self.AB = '' #abstract

path = sys.argv[1]

subpapers = pickle.load(open(path+"subpapers.dump","r"))
IdMatchTopics = pickle.load(open(path + "IdMatchTopics","r"))
CluSimDic = pickle.load(open(path + "CluSimDic","r"))

authorlist = open("../parameter/authorlist","r")
AL = []
for line in authorlist:
    ss = line.split(" ")
    if len(ss)<1: continue
    snew = ss[1][0:len(ss[1])-1] + ", " + ss[0]
    AL.append(snew)

GLscore = {}
entropy = {}
entropy2 = {}
Simp = {}
Gini = {}  # actually 1 - Gini
Shiyan1 = {}

alpha = -0.5
beta = 2

for au in AL:
    subsubpapersID = []
    for p in subpapers:
        if au in p.AU:
            subsubpapersID.append(p.ID)
    tot = {}
    paperN = 0
    ACP = 0
    for ID in subsubpapersID:
        paperN +=1
        ACP += 1
        ss = IdMatchTopics[ID]
        j = 0
        if len(ss)<1: ACP -= 1
        for topic in sorted(ss,key=ss.get,reverse=True):
            j += 1
            #if j>3: break
            if topic in tot:
                tot[topic] += ss[topic]
            else:
                tot[topic] = ss[topic]


    for topic in tot:
        tot[topic] = tot[topic] / ACP
    ns = au.split(", ")
    aunew = ns[1] + " " + ns[0]
    print "The author " + str(aunew) + " has published " +str(paperN) + " papers in ACM."
    j = 0
    print "ACP = ",ACP
    topiclist = {}
    scorelist = {}
    si = 1
    en = 0
    en2 = 0
    sumt = 0
    flag = True
    q1 = 0
    q2 = 0
    totq = 0
    for topic in sorted(tot,key=tot.get,reverse=True):
        j += 1
        if j<=10:  print str(j),topic,str(tot[topic])
        topiclist[j] = topic
        scorelist[j] = tot[topic]
        si -= tot[topic] * tot[topic]
        en -= tot[topic]*math.log(tot[topic],len(tot))
        en2 -= tot[topic]*math.log(tot[topic],2)
        sumt += tot[topic]
    for topic in sorted(tot,key=tot.get,reverse=False):
        q2 = q1 + tot[topic]
        totq = totq + q1 + q2
        q1 = q2
    score = 0
    scope = j
    shiyan1score = 0
    for i in range(1,scope):
        for j in range(i+1,scope):
            if not topiclist[i] in CluSimDic: continue
            if not topiclist[j] in CluSimDic[topiclist[i]]: continue
            si = CluSimDic[topiclist[i]][topiclist[j]]
            score += math.pow(si,alpha) * math.pow(scorelist[i]*scorelist[j],beta)
            shiyan1score += math.pow(si,alpha) * math.pow(scorelist[i]+scorelist[j],beta)
    GLscore[aunew] = score
    entropy[aunew] = en
    entropy2[aunew] = en2
    Simp[aunew] = si
    Gini[aunew] = float(totq)/float(scope)
    Shiyan1[aunew] = shiyan1score
    print "Scope = ",scope
    print

print GLscore

print "Author" + "\t" + "Entropy" + "\t" + "Entropy2" + "\t" + "Simpson" + "\t" + "1-Gini Index" + "\t" + "GLscore" + "\t"  + "Shiyan1"
for au in GLscore:
    print str(au) + "\t" + str(entropy[au]) + "\t" + str(entropy2[au]) + "\t" + str(Simp[au]) + "\t" + str(Gini[au]) + "\t" + str(GLscore[au]) + "\t" + str(Shiyan1[au])
