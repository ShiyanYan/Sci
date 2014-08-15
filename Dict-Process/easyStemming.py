#easyStemming.py run a easy stemming for the dictionary
inpath = "../../DictForPaper/MergedDicGramsNoUniHuman"
infile = open(inpath,"r")
lastline = ""
outpath = "../../DictForPaper/MergedDicGramsNoUniHumanES2"
outfile = open(outpath,"w")
dic = []
for line in infile:
    ss = line[0:len(line)-1]
    if (len(ss)>2) and (ss[len(ss)-1:len(ss)]=='s'):
        ssc = ss[0:len(ss)-1]
        if ssc in dic: continue
        if (ssc[len(ssc)-1:len(ssc)]=='e'):
            sscs = ssc[0:len(ssc)-1]
            if sscs in dic: continue
    dic.append(ss)
for line in dic:
    outfile.write(line + "\n")
outfile.close()
