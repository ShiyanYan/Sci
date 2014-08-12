# the time variation of average author/authors.
import metricesCal
import cPickle as pickle
import sys
import math

subpaperID = []

path = "../../ACMdata/"

IDmatchAuthor = pickle.load(open(path + "ID_AU.dump","rb"))
IDmatchYear = pickle.load(open(path + "ID_Year.dump","rb"))
Authorlist = pickle.load(open(path + "HindexAuthorList.dump","rb"))

path = sys.argv[1]
IDmatchTopics = pickle.load(open(path + "IdMatchTopics","rb"))
AuMatchIDmatchTopics = pickle.load(open(path+"AuMatchIDmatchTopics.dump","rb"))

scoreTot = {} #by  year

totN = {} #by year
cc = 0
for authorname in Authorlist:
    cc += 1
    if cc % 1000 ==0: print str(cc) + " Complete!"
#    if cc>3: break
    if not authorname in AuMatchIDmatchTopics: continue
    for Id in AuMatchIDmatchTopics[authorname]:
        subpaperID.append(Id)

    subIDmatchYear = {}

    for Id in subpaperID:
        if Id in IDmatchYear:
            subIDmatchYear[Id] = IDmatchYear[Id]

    Topics = {}
    paperN = 0
    scores = {}  # by year
    previousYear = 0
    previousscore = []
    scorenow = []
#    mini = []
#    maxi = []
#    for i in range(0,6):
#        mini.append(1000000)
#        maxi.append(0)
    startyear = 2020
    
#    for Id in sorted(subIDmatchYear,key=subIDmatchYear.get,reverse=False):
#        print IDmatchYear[Id],IDmatchTopics[Id]
        
    for Id in sorted(subIDmatchYear,key=subIDmatchYear.get,reverse=False):
        if not Id in AuMatchIDmatchTopics[authorname]: continue
        if len(AuMatchIDmatchTopics[authorname][Id])<=0: continue
        for tot in Topics:
            Topics[tot] = Topics[tot] * float(paperN) / float(paperN+1)
        for tot in AuMatchIDmatchTopics[authorname][Id]:
            if tot in Topics:
                Topics[tot] += AuMatchIDmatchTopics[authorname][Id][tot] *float(1) / float(paperN + 1)
            else:
                Topics[tot] = AuMatchIDmatchTopics[authorname][Id][tot] * float(1) / float(paperN + 1)
        paperN += 1
        YR = IDmatchYear[Id]
        if YR < startyear: 
            startyear = YR
            previousYear = YR
        previousscore = scorenow
        scorenow = metricesCal.MetriCal(Topics)
        if YR == previousYear: continue
        if (YR>=previousYear + 1):
            for year in range(previousYear, YR):
                scores[year-startyear+1] = previousscore
#                print year,previousscore
        previousYear = YR
    #    print previousYear
    #    print scores[YR]
    #    print
    if previousYear==0: continue
    for year in range(previousYear,YR+1):
        scores[year-startyear+1] = scorenow
#        print year,scorenow
#    print
#    print
#    print authorname
#    print scores
    for year in scores:
        if not year in scoreTot:
            scoreTot[year] = []
            for i in range(0,6):
                scoreTot[year].append(0)
        if not year in totN:
            totN[year] = 1
        else:
            totN[year] += 1
        for i in range(0,6):
            scoreTot[year][i] += scores[year][i]

mini = []
maxi = []
for i in range(0,6):
    mini.append(1000000)
    maxi.append(0)

for year in scoreTot:
    for i in range(0,6):
        scoreTot[year][i] = scoreTot[year][i] / float(totN[year])
        if scoreTot[year][i]>maxi[i]: maxi[i] = scoreTot[year][i]
        if scoreTot[year][i]<mini[i]: mini[i] = scoreTot[year][i]


for year in scoreTot:
    print year,scoreTot[year]

print totN
print "Printing the .csv file"

output = open("../../ClusterResultsHumanHH2/metricsAve1.csv","w")
k = 0
scorepre = []
scorenow = []
output.write("Year,Entropy,Entropy2,Simpson,Gini,GLscore,Shiyan1\n")
for year in sorted(scoreTot):
    k += 1
    scorenow = scoreTot[year]
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



        

