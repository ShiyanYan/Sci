#PaperAssignment
import cPickle as pickle
import sys
path = sys.argv[1]
infile = open(path + "Paper_Assignment_Result.txt","rb")
DicForClu = pickle.load(open(path+"DicForClu.dump","rb"))
exemplar = pickle.load(open(path + "exemplar.dump","rb"))
i = 0

ids = ""
IdMatchTopics = {}
k = 0
dic = {}
for line in infile:
    if len(line)<2: continue
    if line[0:2] == "ID":
        k += 1
        if k % 10000 ==0 : print k
        # if k>20: break #
        if ids!="":
            sumt = 0
            for j in dic:
                sumt += dic[j]
            for j in dic:
                dic[j] = float(dic[j]) / float(sumt)

            IdMatchTopics[ids] = dic
            #if k<=10: print dic
        ids = line[3:len(line)-1]
        dic = {}
        flaga = False
        flagf = False
    if flaga:
        ss = line.split("\t")
        for item in ss:
            if item=="": continue
            if not (item in DicForClu): continue
            c = exemplar[DicForClu[item]]
            if c in dic:
                dic[c] +=2
            else:
                dic[c] = 2
        flaga = False
    if flagf:
        ss = line.split("\t")
        for item in ss:
            if item=="": continue
            if not (item in DicForClu): continue
            c = exemplar[DicForClu[item]]
            if c in dic:
                dic[c] +=1
            else:
                dic[c] = 1
        flagf = False
    if line[0:2] == "AB":
        flaga = True
    if line[0:2] == "FT":
    	flagf = True
print k
pickle.dump(IdMatchTopics,open(path + "IdMatchTopics","wb"))
i = 0
for j in IdMatchTopics:
    if len(IdMatchTopics[j])>0: i += 1
    if i>10: break
    if len(IdMatchTopics[j])>0: print j, IdMatchTopics[j]
