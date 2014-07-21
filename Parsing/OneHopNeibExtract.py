#OneHopNeibExtract.py
import cPickle as pickle
dicin = "../../DicForPaper/CategoryTermsSortedNoUniHuman"
for line in open(dicin,"r"):
    dic.append(line[0:len(line)-1])
dic = sorted(dic)

outdic = []
def isInDic(term):
    i = 0
    j = len(dic)-1
    while True:
        if i>=j: break
        mid = (i+j) / 2
        if dic[mid] == term: return True
        if term <= dic[mid]:
            j = mid
        else:
            i = mid + 1
    if dic[mid] == term: 
        return True
    else:
        return False

path = "../../Wiki/Category/"
infile = open(path + "categorylinks","rb")
for line in infile:
    ss = line.split("\t")
    ss[1] = ss[1][0:len(ss[1])-1]
    flag1 = False
    flag2 = False
    if isInDic(ss[0]): flag1 = True
    if isInDic(ss[1]): flag2 = True
    if flag1 and (not flag2): outdic.append(ss[1])
    if flag2 and (not flag1): outdic.append(ss[0])

outdic = sorted(outdic)
lastterm = ""
out = []
outfile = open("../../DicForPaper/","w")
for term in outdic:
    if (term == lastterm): continue
    out.append(term)
    outfile.write(term+"\n")
    lastterm = term



print "Total= ",len(out)