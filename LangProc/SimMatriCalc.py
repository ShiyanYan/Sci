#Similarity matrix Calculation
import cPickle as pickle
import math
import sys
syspath = sys.argv[1]
dic = pickle.load(open(syspath+"dict","r"))
i = 1
dicts = {}
dictss = {}
for t in dic:
    dicts[t] = i
    dictss[i] = t
    i += 1
dicRange = i-1

outdic= open(syspath+"outdic","w")
pickle.dump(dictss,outdic)
print dicRange
matr = {}
flag = True
for i in range(1,dicRange+2):
    matr[i] = []
    matr[i].append(0)
    for j in range(1,dicRange+2):
        if (i==j): 
            if flag:
                print i,j
                flag = False
            matr[i].append(1)
        else:
            matr[i].append(0)
print len(matr)
infile = open(syspath+"word-links","r")
for line in infile:
    ss = line.split("\t")
    num1 = dicts[ss[0]]
    num2 = dicts[ss[1]]
    cc = int(ss[2][0:len(ss[2])-1])
    # print ss
    # print num1,num2
    if (num1<=0) or (num2<=0): print num1, num2
    if (num1>dicRange) or (num2>dicRange): print num1,num2
    matr[num1][num2] += math.log(cc+1,2)/math.log(26000,2)
    matr[num2][num1] += math.log(cc+1,2)/math.log(26000,2)

print len(dicts)
# pickle.dump(matr,open(syspath+"simMatrix","w"))
# pickle.dump(dicts,open(syspath+"wordMatchNum","w"))

# outfile = open(syspath+"sim","w")
# for i in range(0,dicRange):
#     word = dic[i].replace(" ","_")
#     if i==dicRange-1:
#         outfile.write(word + "\n")
#     else:
#         outfile.write(word + " ")
outfile2 = open(syspath+"similarityFile","w")
x = 0
for i in range(1,dicRange+1):
    for j in range(1,dicRange+1):
        if (matr[i][j]>=0):
            x += matr[i][j] 
            outfile2(str(i)+"  "+str(j) + "  " + str(matr[i][j]) + "\n")

outfile2.close()

outfile3 = open(syspath+"summary","w")
outfile3.write("number of grams\n")
outfile.write(str(dicRange)+"\n")
outfile3.write("average\n")
outfile3.write(str(x/dicRange/dicRange))
outfile3.close()

# for i in range(1,dicRange+1):
#     for j in range(1,dicRange+1):
#         if (j==dicRange):
#             outfile.write( str(matr[i][j]) + "\n")
#         else:
#             outfile.write( str(matr[i][j]) + " ")

# outfile.close()
