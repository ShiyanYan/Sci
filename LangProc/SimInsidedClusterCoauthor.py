#SimInsidedClusterCoauthor.py
import sys
import cPickle as pickle 
import math

class Paper:
    #ID   #AU [] 
    def __init__(self):
        self.ID = ''
        self.AU = []

# Read the paper ID & AU
paperPath = "../../ACMdata/ID_AU_AF"
papers = []
def readPaperFromFile(File):
    inFile = open(str(File), "r")
    InitialNumberOfPapers = 0
    PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
    p = Paper()
    abflag = 0
    authorflag = 0
    i = 0
    for lines in inFile:
        i += 1
        #if i%100000 == 0: print "Proc " + str(i) + " Complete"
        string = str(lines)
        # if(string =='\n' or string ==' \n'):
        #     PaperFlag = 0
        #     papers.append(p)
        #     p = Paper()
        #     continue
        if(string[0] == 'I' and string[1]=='D'):
            if PaperFlag==1: 
                papers.append(p)
                p = Paper()
            PaperFlag = 1
            #processing ID
            l = len(string)
            p.ID = string[3:l-1]
        elif(string[0] == 'A' and string[1]=='U'):
            l = len(string)
            s = string[3:l-1]  
            p.AU.append(s)
        elif((string[0] == ' ') and (PaperFlag==1)):
            l = len(string)
            s = string[1:l-1]     
            p.AU.append(s)

print "Begin paper ID and Author list Reading"
readPaperFromFile(paperPath)

print "End of Reading"

path = "../../ClusterResultsHumanHH2/"

IdMatchTopics = pickle.load(open(path + "IdMatchTopics","r"))

print "Begin the process: Author Match Topics"


AuthorMatchTopics = {}
PaperNum = {}
for p in papers:
    Id = p.ID 
    Aulist = p.AU
    Topics = IdMatchTopics[Id]
    for au in Aulist:
        if au in PaperNum:
            PaperNum[au] += 1
        else:
            PaperNum[au] = 1
        if not au in AuthorMatchTopics:
            AuthorMatchTopics[au] = {}
        for tot in Topics:
            if tot in AuthorMatchTopics[au]:
                AuthorMatchTopics[au][tot] += Topics[tot]
            else:
                AuthorMatchTopics[au][tot] = Topics[tot]

AuthorMatchMajorTopics = {}


print "Begin the process: Find the major topics"

for au in AuthorMatchTopics:
    paperN = float(PaperNum[au])
    for tot in AuthorMatchTopics[au]:
        AuthorMatchTopics[au][tot] = float(AuthorMatchTopics[au][tot]/paperN)
    i = 0
    for tot in sorted(AuthorMatchTopics[au],key=AuthorMatchTopics[au].get,reverse=True):
        i += 1
        if i>2: break
        if AuthorMatchTopics[au][tot]<0.3: break
        AuthorMatchMajorTopics[au].append(tot)

SumOfPaperCohe = {}
NumOfPaperCohe = {}

print "Begin the process: Calculate the coauthor porportion"

for p in papers:
    Id = p.ID 
    Aulist = p.AU  # authors should be in the AuthorMatchMajorTopics list first.
    Topics = IdMatchTopics[Id]
    i = 0
    PaperMajorTopic = ""
    for tot in sorted(Topics,key=Topics.get,reverse=True):
        i += 1
        if i>1: break
        if Topics[tot] > 0.5: PaperMajorTopic = tot
    if PaperMajorTopic == "": continue
    if PaperMajorTopic in NumOfPaperCohe:
        NumOfPaperCohe[PaperMajorTopic] += 1
    else:
        NumOfPaperCohe[PaperMajorTopic] = 1
    tt = 0
    for au in Aulist:
        if not au in AuthorMatchMajorTopics: continue
        if PaperMajorTopic in AuthorMatchMajorTopics[au]: tt += 1
    porp = float(tt) / float(len(Aulist))

    if PaperMajorTopic in SumOfPaperCohe:
        SumOfPaperCohe[PaperMajorTopic] += porp
    else:
        SumOfPaperCohe[PaperMajorTopic] = porp


for tot in SumOfPaperCohe:
    SumOfPaperCohe[tot] = float(SumOfPaperCohe[tot]) / float(NumOfPaperCohe[tot])

print "Begin writing"

outputdump = open(path + "SimInsideCoauthor.dump","wb")

pickle.dump(SumOfPaperCohe,outputdump)

output = open(path + "SimInsideCoauthor.txt","wb")

for tot in sorted(SumOfPaperCohe,key=SumOfPaperCohe.get,reverse = True):
    output.write(tot + " " + str(SumOfPaperCohe[tot]) + "\n")

output.close()

print "Done!"

# assign the authors

#calculate the pairs porportion 