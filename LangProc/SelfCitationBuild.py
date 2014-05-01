#Self-Citation Network Building
import networkx as nx
import pickle
IdMatchTopics = {}
IdMatchTopics = pickle.load(open("../../ACMdata/IdMatchTopics","r"))
IDmatchScore = {}
infile1 = open("../../ACMdata/IdMatchScore","r")
IDmatchScore = pickle.load(infile1)

class Paper:
    #ID
    #CI
    #SO
    #TI
    #BI
    #AU []
    #AF []
    #CT []
    #CO []
    #RF []
    #CA []
    #YR
    #AB
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

papers = [] # the set of all papers
subpapers = [] # papers of a particular author
IDmatchPapers = {} # the ID match papers dictionary
AuthorName = "Lagoze, C" # the name of the author of the self-citation network
def readPaperFromFile(File):
    inFile = open(str(File), "r")
    InitialNumberOfPapers = 0
    PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
    p = Paper()
    abflag = 0
    authorflag = 0
    for lines in inFile:
        string = str(lines)
        if(string =='\n' or string ==' \n'):
            PaperFlag = 0
            papers.append(p)
            IDmatchPapers[p.ID] = p
            InitialNumberOfPapers = InitialNumberOfPapers +1
            if (authorflag == 1):
               subpapers.append(p)
               authorflag = 0
            p = Paper()
            continue
        if (abflag == 1):
            p.AB = string
            abflag = 0
            continue
        if(string[0] == 'I' and string[1]=='D'):
            PaperFlag = 1
            #processing ID
            l = len(string)
            p.ID = string[3:l-1]
        elif(string[0] == 'C' and string[1]=='I'):
            #processing CI
            l = len(string)
            p.CI = string[3:l-1]
        elif(string[0] == 'S' and string[1]=='O'):
            #processing SO
            l = len(string)
            p.SO = string[3:l-1]
        elif(string[0] == 'T' and string[1]=='I'):
            #processing TI
            l = len(string)
            p.TI = string[3:l-1]
        elif(string[0] == 'B' and string[1]=='I'):
            #processing BI and Year
            l = len(string)
            p.BI = string[3:l-1]
            temp = string[l-5:l-1]
            p.YR  = int(temp)
        elif(string[0] == 'A' and string[1]=='U'):
            l = len(string)
            s = string[3:l-1]
            if (s == AuthorName):
                authorflag = 1    
            p.AU.append(s)
        elif((string[0] == ' ') and (PaperFlag==1)):
            l = len(string)
            s = string[1:l-1]
            if (s == AuthorName):
                authorflag = 1      
            p.AU.append(s)
        elif(string[0] == 'A' and string[1]=='F'):
            #processing AF
            l = len(string)
            s = string[3:l-1]
            p.AF.append(s)
        elif(string[0] == 'C' and string[1]=='T'):
            #processing CT
            l = len(string)
            s = string[3:l-1]
            p.CT.append(s)
        elif(string[0] == 'C' and string[1]=='O'):
            #processing CO
            l = len(string)
            s = string[3:l-1]
            p.CO.append(s)
        elif(string[0] == 'R' and string[1]=='F'):
            #processing RF
            l = len(string)
            s = string[3:l-1]
            p.RF.append(s)
        elif(string[0] == 'C' and string[1]=='A'):
            #processing CA
            l = len(string)
            s = string[3:l-1]
            p.CA.append(s)
        elif(string[0] == 'A' and string[1]=='B'):
            # processing AB
            abflag = 1
            
    inFile.close()
    print 'Read Complete'    
readPaperFromFile("../../ACMdata/in.txt")
G = nx.Graph()
paperMatch = {}
i = 0
Idlist = []  # prevent the citation to the same papers
for p in subpapers:
    i += 1
    paperMatch[i] = p
    Idlist.append(p.ID)
    G.add_node(i)
totself = i
print "The Author write " +str(totself) + " papers"
# Detect the indirect relationship
for p in subpapers:
    for ref in p.RF:
        if not (ref in IDmatchPapers): continue
        pt = IDmatchPapers[ref]
        flagg = False
        for refpt in pt.RF:
            if not (refpt in IDmatchPapers): continue
            ptt = IDmatchPapers[refpt]
            if AuthorName in ptt.AU:
                flagg = True
                break
        if flagg:
            if not (pt.ID in Idlist):
                i += 1
                paperMatch[i] = pt
                G.add_node(i)
                Idlist.append(pt.ID)
            flagg = False
    
tot = i
print "There are " + str(tot) + " papers in the network"
for i in range(1,tot+1):
    for j in range(1, tot+1):
        if (i==j): continue
        for ref in paperMatch[i].RF:
            if (ref == paperMatch[j].ID):
                G.add_edge(i,j)
k = 0
for ID in Idlist:
    k += 1
    print str(k),IDmatchPapers[ID].TI
print nx.connected_components(G)
print G.nodes()
print G.edges()
clusters = nx.clustering(G)
clu = {}
tt = 0
for sets in nx.connected_components(G):
    tt += 1
    clu[tt] = []
    for ss in sets:
        clu[tt].append(ss)
# for x in clusters:
#     if clusters[x] in clu:
#         clu[clusters[x]].append(x)
#     else:
#         clu[clusters[x]] = []
#         clu[clusters[x]].append(x)
i = 0
for t in clu:
    i += 1
    print "Information of Cluster " + str(i)
    papIDs = clu[t]
    j = 0
    print "---------"
    for pi in papIDs:
        j += 1
        pap = paperMatch[pi]
        print "paper" + str(i) + "." + str(j) + "paperID=" + str(pap.ID) + " paperTI=" + str(pap.TI)
        if pap.ID in IdMatchTopics: print(IdMatchTopics[pap.ID])
        # if not (pap.ID in IDmatchScore): continue
        # scoreset = IDmatchScore[pap.ID]        
        # tt = 0
        # for t in sorted(scoreset, key=scoreset.get, reverse=True):
        #     tt +=1
        #     if tt>10: break
        #     print t,scoreset[t]
        # print ".."
    print "--------"



