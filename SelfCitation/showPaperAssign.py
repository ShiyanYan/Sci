import cPickle as pickle
IdMatchTopics = pickle.load(open("../../ACMdata/IdMatchTopics","r"))
subpapers = pickle.load(open("../../ACMdata/SubPapers.dump"),"r")

i = 0
for p in subpapers:
    i += 1
    print "Paper ",i
    print "ID = ",p.ID
    print "Title = ",p.TI
    ss = IdMatchTopics[p.ID]
    j = 0
    Assign = ""
    for k in sorted(ss,key=ss.get(),reverse=True):
        j += 1
        if j>3: break
        Assign += str(k) + " " + str(ss[k]) + " "
    print Assign
    print