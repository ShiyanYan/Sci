#testRead.py
import cPickle as pickle
print "begin"
infile = open("../../ACMdata/AuthorList_all.dump","r")
dic = pickle.load(infile)
t = 0
outfile = open("../../ACMdata/AuthorList_above5.dump","wb")
print len(dic)
dic2 = {}
for tt in sorted(dic,key=dic.get,reverse=True):
    if t<1000: print tt,dic[tt]
    t += 1
    dic2[tt] = dic[tt]
    if dic[tt]<5:
         print t
         break
pickle.dump(dic2,outfile)

"""
dic2 = {}
for tt in sorted(dic,key=dic.get,reverse=True):
    t += 1
    #if t>1000: break
    if tt.find(" ")== -1: continue
    dic2[tt] = dic[tt]

t = 0
outfile = open("../../ACMdata/Test4","w")
for tt in sorted(dic2,key=dic2.get,reverse=True):
    t += 1
    #if t>1000: break
    if dic2[tt]<=5: break
    outfile.write(str(tt)+" "+str(dic[tt])+"\n")
"""
     
