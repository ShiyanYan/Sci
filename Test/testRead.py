#testRead.py
import pickle
print "begin"
infile = open("../../ACMdata/NofGram2","r")
dic = pickle.load(infile)
t = 0
print len(dic)
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
     
