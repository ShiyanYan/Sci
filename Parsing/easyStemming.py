#easyStemming.py run a easy stemming for the dictionary
inpath = "../../DictForPaper/MergedDicGramsNoUni"
infile = open(inpath,"r")
lastline = ""
outpath = "../../DictForPaper/MergedDicGramsNoUniES"
outfile = open(outpath,"w")
for line in infile:
    ss = line[0:len(line)-1]
    ssc = lastline + "s"
    sscs = lastline + "es"
    if (ss!=ssc) and (ss!=sscs):
        outfile.write(ss + "\n")
    lastline = ss
outfile.close()