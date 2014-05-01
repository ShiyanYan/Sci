#abbrev detection
dic = []
import cPickle as pickle
with open("../../DictForPaper/CategoryTermsSortedNoUni","rb") as f:
    for line in f:
        w = line[0:len(line)-1]
        dic.append(w)

out = open("../../DictForPaper/AbbMatch","wb") # abbreviation lists

abbdic = {}
with open("../../Wiki/abbrvs.count","rb") as f:
    i = 0
    for line in f:
        i += 1
        ss = line.split("\t")
        wh = ss[1][0:len(ss[1])-1]
        ss2 = ss[0].split(" ")
        ab = ss2[len(ss2)-1]
        if wh in dic:
            abbdic[wh] = ab

out1 = open("../../DictForPaper/AbMatchGrams","wb")
out2 = open("../../DictForPaper/WholeMatchAb","wb")
dic1 = {}
dic2 = {}
for w in abbdic:
    dic1[abbdic[w]] = w
    w1 = w + " " + abbdic[w]
    w2 = abbdic[w] + " " + w
    dic2[w1] = abbdic[w]
    dic2[w2] = abbdic[w]
    out.write(abbdic[w]+"\t" + w + "\n")
print len(dic1)
print len(dic2)
pickle.dump(dic1,out1)
pickle.dump(dic2,out2)

out.close()

