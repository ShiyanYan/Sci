import cPickle as pickle
path = "../../ClusterResults/"
dic = pickle.load(open(path+"outdic","r"))
i = 0

assign = {}
with open(path+"apcluster/idx.txt","r") as f:
    for line in f:
        i += 1
        k = int(line[0:len(line)-1])
        if k in assign:
            assign[k].append(i)
        else:
            assign[k] = []
            assign[k].append(i)
i = 0
with open(path+"apcluster/ResultsText.txt","w") as f:
    for item in assign:
        ex = dic(item)
        i +=1 
        f.write("Cluster " + str(i) + " exemplar:" + ex + "\n")
        for it in assign[item]:
            ss = dic[it].replace(" ","_")
            f.write(ss + "\t")
        f.write("\n")