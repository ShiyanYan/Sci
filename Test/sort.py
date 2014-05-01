#sort
listt = []
infile = open("../../DictForPaper/CategoryTerms2","rb")
for line in infile:
    s = line[0:len(line)-1]
    if not (s in listt):
        listt.append(s)
outfile = open("../../DictForPaper/CategoryTerms2Sorted",'w')
for t in sorted(listt):
    outfile.write(t + "\n")
outfile.close()