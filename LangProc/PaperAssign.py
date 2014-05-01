#PaperAssignment
import pickle
infile = open("../../ACMdata/wordlist-fulltext.txt","rb")
DicForClu = pickle.load(open("../../ACMdata/DicForClu","rb"))
exemplar = pickle.load(open("../../ACMdata/exemplar","rb"))

ids = ""
IdMatchTopics = {}
k = 0
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
pickle.dump(IdMatchTopics,open("../../ACMdata/IdMatchTopics","wb"))
# for j in IdMatchTopics:
#     print j, IdMatchTopics[j]