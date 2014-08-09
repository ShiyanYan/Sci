import sys
import cPickle as pickle
import math

path = "../../ACMdata/"

AuMatchHindex = pickle.load(open(path + "HindexResults.dump","rb"))
AuNameMatch = pickle.load(open(path + "HindexAuthorList.dump","rb"))

path = "../../ClusterResultsHumanHH2/"
AuMatchScores = pickle.load(open(path + "AuMatchScores.dump","rb"))


output = open(path + "ScoresHindexNoAu.csv" ,"wb")

startline = "Entropy,Entropy2,Simpson,Gini,GLscore,Shiyan1,"

startline = startline + "CitNum,CitNum09,Hin,Hin09,I10,I1009\n"

output.write(startline)
for au in AuMatchScores:
    if not au in AuNameMatch: continue
    aum = ""
    if len(AuNameMatch[au])!=1: continue
    for kk in AuNameMatch[au]:
        aum = kk
    if not aum in AuMatchHindex: continue
  #  output.write(str(aum)+",")
    for score in AuMatchScores[au]:
        output.write(str(score) + ",")
    j = 0
    for score in AuMatchHindex[aum]:
        j += 1
        output.write(str(score))
        if j<=5: output.write(",")
        else: output.write("\n")

output.close()  

