#conceptIdExtract
import cPickle as pickle
path = "../../Wiki/Category/"
infile = open(path + "categorylinks","rb")
listterm = []
dic = {}
i = 0
for line in infile:
    i += 1
    if (i % 1000000 == 0): print "Complete Line" + str(i)
    s = line.split("\t")
    s[1] = s[1][0:len(s[1])-1]
    if not (s[0] in listterm): listterm.append(s[0])
    if not (s[1] in listterm): listterm.append(s[1])
infile.close()

listterm = sorted(listterm)
outfile = open(path + "termDic","wb")
i = 0 
for term in listterm:
    i += 1
    dic[term] = i
    if (term == "computer science"): print "computer science",i
    outfile.write(term + " " + str(i) + "\n")
outfile.close()

print "Writing"
outfile2 = open(path + "/NumberLinkList","wb")
infile = open(path + "categorylinks","rb")
for line in infile:
    i += 1
    if (i % 1000000 == 0): print "Complete Line" + str(i)
    s = line.split("\t")
    s[1] = s[1][0:len(s[1])-1]
    id1 = dic[s[0]]
    id2 = dic[s[1]]
    outfile2.write(str(id1) + "\t" + str(id2) + "\n")
outfile2.close()

