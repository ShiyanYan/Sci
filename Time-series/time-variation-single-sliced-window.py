# the time variation of single author with a sliced window
import metricesCal
import cPickle as pickle
import sys
import math
authorname = "Carl   Lagoze"

MetricsN = 7


window = 5
subpaperID = []

path = "../../ACMdata/"

IDmatchAuthor = pickle.load(open(path + "ID_AU.dump","rb"))
IDmatchYear = pickle.load(open(path + "ID_Year.dump","rb"))

path = "../../ClusterResultsHumanHH2/"
IDmatchTopics = pickle.load(open(path + "IdMatchTopics","rb")) ##

metricsNames = []

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


chroIDlist = sorted(subIDmatchYear,key=subIDmatchYear.get,reverse=False)

startyear = subIDmatchYear(chroIDlist[0])

endyear = subIDmatchYear(chroIDlist[len(chroIDlist)-1])

li = 0
ri = 0 
IDlistNow = []


mini = []
maxi = []

scores = {}

for i in range(0,MetricsN):
    mini.append(100)
    maxi.append(0)

for st in range(startyear,endyear-window+2):
    ed = st + window -1
    while (ri<=len(chroIDlist)-1) and (subIDmatchYear[chroIDlist[ri]]<=ed):
        IDlistNow.append(chroIDlist[ri])
        ri += 1
    while subIDmatchYear[chroIDlist[li]]<st:
        IDlistNow.remove(chroIDlist[li])
        li += 1
    Topics = 0
    for ids in IDlistNow:
        tot = dict(IdMatchTopics[ids])
        for evtot in tot:
            if evtot in Topics: 
                Topics[evtot] += tot[evtot]
            else:
                Topics[evtot] = tot[evtot]
    for evtot in Topics:
        Topics[evtot] = float(Topics[evtot]) / float(len(IDlistNow))
    scorenow =list(metricesCal.MetriCal(Topics))
    for i in range(0,MetricsN):
        if scorenow[i]>maxi[i]: maxi[i] = scorenow[i]
        if scorenow[i]<mini[i]: mini[i] = scorenow[i]

    scores[st] = scorenow


print "Printing the .csv file"

output = open(path + "5years_sliced_" + authorname + ".csv","w")
k = 0
scorepre = []
scorenow = []

output.write("Year")

for name in metricsNames:
    output.write("," + metricsNames[name])

output.write("\n")

for year in sorted(scores):
    k += 1
    output.write(str(year) + ",")
    scorenow = scores[year]
    for i in range(0,MetricsN):
        scorenow[i] = (scorenow[i] - mini[i]) / (maxi[i] - mini[i])
        output.write(str(scorenow[i]))
        if (i==MetricsN-1):
            output.write("\n")
        else:
            output.write(",")
    
output.close()



        

