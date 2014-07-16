#Extract papers from one author
import cPickle as pickle
import sys
AuthorName = sys.argv[2] + ", " + sys.argv[1]
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

subpapers = []

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
        if(string =='\n' or string ==' \n'):
            PaperFlag = 0
            #papers.append(p)
#            IDmatchPapers[p.ID] = p
            InitialNumberOfPapers = InitialNumberOfPapers +1
            if (authorflag == 1):
               subpapers.append(p)
               authorflag = 0
            p = Paper()
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
            #p.YR  = int(temp)
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

readPaperFromFile(sys.argv[3])
fout = open(sys.argv[4]+"SubPapers.dump","wb")
pickle.dump(subpapers,fout)
i = 0
for p in subpapers:
    i += 1
    print "Paper ",i
    print p.ID
    print p.TI
    print p.AU
