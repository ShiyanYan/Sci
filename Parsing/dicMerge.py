#dicMerge.py
infile2 = open("../../Wiki/abbrvs.count.out")
infile1 = open("../../ACMdata/test","r")
dic1 = []
dic2 = []
for t in infile1:
    dic1.append(t[0:len(t)-1])
dic1 = sorted(dic1)
df = []
cc = 0
print "Begin Reading"
for t in infile2:
    t = t[0:len(t)-1]
    cc += 1
    if (cc % 10000==0): print "Complete" + str(cc)
    i = 0
    j = len(dic1)-1
    flag = False
    while (i<j):
        mid = (i+j) / 2
        if (dic1[mid]==t): flag = True
        if dic1[mid]>=t:
            j= mid
        else:
            i = mid + 1
    if (dic1[mid]==t): flag = True
    if flag: df.append(t)

outfile = open("../../ACMdata/output/combinedDicNoisyVersion","w")
df = sorted(df)
ff = False
dfs = []
for k in df:
    if not ff:
    	dfs.append(k)
    	lastk = k
        ff = True
        continue
    if (k==lastk): continue
    dfs.append(k)
    lastk = k
df = dfs
for t in df:
    outfile.write(t+"\n")
outfile.close()