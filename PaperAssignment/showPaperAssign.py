# also paper assignment
import cPickle as pickle
import sys
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
IdMatchTopics = pickle.load(open(path + "IdMatchTopics","r"))
subpapers = pickle.load(open(path + "SubPapers.dump","r"))

 
i = 0
tot = {}
for p in subpapers:
    i += 1
    print "Paper ",i
    print "ID = ",p.ID
    print "Title = ",p.TI
    ss = IdMatchTopics[p.ID]
    if len(ss)==0: continue
    j = 0
    Assign = ""
    for k in sorted(ss,key=ss.get,reverse=True):
        j += 1
        if k in tot:
            tot[k] += ss[k]
        else:
            tot[k] = ss[k]
        if j<=3:
            Assign += str(k) + " " + str(ss[k]) + " "
    print Assign
    print

for t in tot:
    tot[t] = tot[t] / i

print "OverAll, the author published " + str(i) + " papers"
print "Assignment over Topics"
Assign = ""
j = 0
for k in sorted(tot, key=tot.get,reverse=True):
    j += 1
    if j<=10:
        Assign += str(j) + "\t" +  str(k) + "\t" + str(tot[k]) + "\n"
print Assign
