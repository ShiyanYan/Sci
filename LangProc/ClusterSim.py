#ClusterSim.py
import pickle
DicForClu = pickle.load(open("../../ACMdata/DicForClu","rb"))
exemplar = pickle.load(open("../../ACMdata/exemplar","rb"))
wordMatchNum = pickle.load(open("../../ACMdata/output/wordMatchNum","r"))

matr = pickle.load(open("../../ACMdata/output/simMatrix","r"))
print(wordMatchNum)
print len(wordMatchNum)
cluTT = 0
cluMatchTerm = {}
t = 0
for kk in DicForClu:
    t += 1
    clunum = DicForClu[kk]
    if clunum>cluTT: cluTT = clunum
    if clunum in cluMatchTerm:
        cluMatchTerm[clunum].append(kk)
    else:
        cluMatchTerm[clunum] = []
        cluMatchTerm[clunum].append(kk)

print t
print cluMatchTerm

cluMatrix = {}
for i in range(1,cluTT+2):
    cluMatrix[i] = []
    cluMatrix[i].append(0)
    for j in range(1,cluTT+2):
        if (i==j): 
            cluMatrix[i].append(1)
        else:
            cluMatrix[i].append(0)
# initialization

print cluTT
for i in range(1,cluTT+1):
    if not (i in cluMatchTerm): continue
    listOfTerms1 = cluMatchTerm[i]
    max1 = 0
    max2 = 0
    nearL = 1
    nearL2 = 1
    for j in range(1,cluTT+1):
        if i==j: continue
        if not (j in cluMatchTerm): continue
        listOfTerms2 = cluMatchTerm[j]
        TT = 0
        sumAve = 0
        for t1 in listOfTerms1:
            for t2 in listOfTerms2:
                
                t1 = t1.replace("_"," ")
                t2 = t2.replace("_"," ")
                if not (t1 in wordMatchNum): continue
                if not (t2 in wordMatchNum): continue
                TT += 1
                sumAve += matr[wordMatchNum[t1]][wordMatchNum[t2]]
        ave = float(sumAve) / float(TT)
        cluMatrix[i][j] = ave
        if ave>max1:
            max2 = max1
            nearL2 = nearL
            max1 = ave
            nearL = exemplar[j]
            continue
        if ave>max2:
            max2 = ave
            nearL2 = exemplar[j]
    print exemplar[i],nearL,nearL2

