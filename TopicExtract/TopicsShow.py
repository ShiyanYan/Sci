import cPickle as pickle
path = "../../ClusterResults/"
dic = pickle.load(open(path+"outdic","r"))
i = 0
print len(dic)
assign = {}
with open(path+"apcluster/idx.txt","r") as f:
    for line in f:
        i += 1
        k = int(line[0:len(line)-1])
        if (k<=0): continue
        if k in assign:
            assign[k].append(i)
        else:
            assign[k] = []
            assign[k].append(i)
i = 0
with open(path+"apcluster/ResultsText2.txt","w") as f:
    for item in assign:
        if len(assign[item])<=2: continue
        ex = dic[item]
        i +=1
        f.write("------------------\n") 
        f.write("Cluster " + str(i) + " exemplar:" + ex + "\n")
        for it in assign[item]:
            ss = dic[it].replace(" ","_")
            f.write(ss + "\t")
        f.write("\n")

i = 0
outfile1 = open(path+"exemplar.dump","wb")
outfile2 = open(path+"DicForClu.dump","wb")
exemplar = []
exemplar.append("0")
DicForClu = {}
for item in assign:
    i += 1
    ex = dic[item]
    exemplar.append(ex)
    for it in assign[item]:
        DicForClu[dic[it]] = i
i = 0
for it in exemplar:
    i += 1
    if i>10: break
    print i,it,exemplar[i-1]
i = 0
for it in DicForClu:
    i += 1
    if i>10: break
    print i, it, DicForClu[it]
print len(exemplar),len(DicForClu)
pickle.dump(exemplar,outfile1)
pickle.dump(DicForClu,outfile2)

    
