# Generate the final scores for every metric
import metricesCal
import sys
import cPickle as pickle
import math

path = "../../ACMdata/"

Authorlist = pickle.load(open(path + "HindexAuthorList.dump","rb"))

path = "../../ClusterResultsHumanHH2/"
AuMatchIDmatchTopics = pickle.load(open(path+"AuMatchIDmatchTopics.dump","rb"))



output = open(path + "AuMatchScores.dump","wb")

AuMatchScores = {}

cc = 0
for au in Authorlist:
    cc += 1
    if cc % 1000==0: print str(cc) + " Complete!"
    if not au in AuMatchIDmatchTopics: continue
    Topics = {}
    IdmatchTopics = AuMatchIDmatchTopics[au]
    if len(IdmatchTopics)<1: continue
    for Id in IdmatchTopics:
        for tot in IdmatchTopics[Id]:
             if tot in Topics: Topics[tot] += IdmatchTopics[Id][tot]
             else: Topics[tot] = IdmatchTopics[Id][tot]
    for tot in Topics:
        Topics[tot] = float(Topics[tot]) / float(len(IdmatchTopics))
    if len(Topics)<1: continue
    scores = metricesCal.MetriCal(Topics)
    AuMatchScores[au] = scores

pickle.dump(AuMatchScores,output)
