# The codes to generate the ClosestArea files from CluSimDic

import sys
import cPickle as pickle

path = "../../ClusterResultsHumanHH2/"

CluSimDic = pickle.load(open(path + "CluSimDic","r"))

ClosestAreaList = {}

for tot in CluSimDic:
    ClosestArea = ""
    ClosestArea2 = ""
    Hst = -500
    Hst2 = -1000
    ClosestAreaList[tot] = {} 
    for tot2 in CluSimDic[tot]:
        if CluSimDic[tot][tot2]>Hst:
            Hst2 = Hst
            Hst = CluSimDic[tot][tot2]
            ClosestArea2 = ClosestArea
            ClosestArea = tot2
            continue
        if CluSimDic[tot][tot2]>Hst2:
            Hst2 = CluSimDic[tot][tot2]
            ClosestArea2 = tot2
    ClosestAreaList[tot][ClosestArea] = Hst
    ClosestAreaList[tot][ClosestArea2] = Hst2

output = open(path + "ClosestArea.dump","w")
pickle.dump(ClosestAreaList,output)

