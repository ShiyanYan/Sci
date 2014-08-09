# the time variation of single author/authors.
import metricesCal
import cPickle as pickle
import sys
import math
authorname = "Carl   Lagoze"

subpaperID = []

path = "../../ACMdata/"

IDmatchAuthor = pickle.load(open(path + "ID_AU.dump","rb"))
IDmatchTopics = pickle.load(open("../../ClusterResultsHumanHH2/IdMatchTopics","rb")) ##
IDmatchYear = pickle.load(open(path + "ID_Year.dump","rb"))


for Id in IDmatchAuthor:
    if authorname in IDmatchAuthor[Id]:
        subpaperID.append(Id)

subIDmatchYear = {}

for Id in subpaperID:
    if Id in IDmatchYear:
        subIDmatchYear[Id] = IDmatchYear[Id]

Topics = {}
paperN = 0
scores = {}  # by year
previousYear = 0
mini = []
maxi = []
for i in range(0,6):
    mini.append(100)
    maxi.append(0)

for Id in sorted(subIDmatchYear,key=subIDmatchYear.get,reverse=False):
    if not Id in IDmatchTopics: continue
    if len(IDmatchTopics[Id])<=0: continue
    #print IDmatchTopics[Id]
    for tot in Topics:
        Topics[tot] = Topics[tot] * float(paperN) / float(paperN+1)
    for tot in IDmatchTopics[Id]:
        if tot in Topics:
            Topics[tot] += IDmatchTopics[Id][tot] *float(1) / float(paperN + 1)
        else:
            Topics[tot] = IDmatchTopics[Id][tot] * float(1) / float(paperN + 1)
    paperN += 1
    YR = IDmatchYear[Id]
    if YR == previousYear: continue
    scorenow = metricesCal.MetriCal(Topics)
    for i in range(0,6):
        if scorenow[i]>maxi[i]: maxi[i] = scorenow[i]
        if scorenow[i]<mini[i]: mini[i] = scorenow[i]
    scores[YR] = scorenow
    previousYear = YR
#    print previousYear
#    print scores[YR]
#    print   

print "Printing the .csv file"

output = open("../../ClusterResultsHumanHH2/metrics.csv","w")
k = 0
scorepre = []
scorenow = []
output.write("Year,Entropy,Entropy2,Simpson,Gini,GLscore,Shiyan1\n")
for year in sorted(scores):
    k += 1
    scorenow = scores[year]
    for i in range(0,6):
        scorenow[i] = (scorenow[i] - mini[i]) / (maxi[i] - mini[i])
    if k==1: startyear = year
    for byear in range(startyear,year):
        output.write(str(byear) + ",")
        for i in range(0,6):
            if i<5: 
                output.write(str(scorepre[i]) + ",")
            else:
                output.write(str(scorepre[i]) + "\n")
    output.write(str(year) + ",")
    for i in range(0,6):
        if i<5:
            output.write(str(scorenow[i]) + ",")
        else:
            output.write(str(scorenow[i]) + "\n")
    scorepre = scorenow
    startyear = year + 1

output.close()



        

