# the code to generate the dictionary for Author match IDmatchTopics.

import sys
import cPickle as pickle
import math
path = "../../ACMdata/"

IDmatchAuthor = pickle.load(open(path + "ID_AU.dump","rb"))
Authorlist = pickle.load(open(path + "HindexAuthorList.dump","rb"))

path = "../../ClusterResultsHumanHH2/"
IDmatchTopics = pickle.load(open(path + "IdMatchTopics","rb"))


AuMatchIDmatchTopics = {}
cc = 0
for Id in IDmatchAuthor:
    cc += 1
    if cc % 100000==0: print str(cc) + " Complete!"
    for au in IDmatchAuthor[Id]:
        if not au in Authorlist: continue
        if not au in AuMatchIDmatchTopics: AuMatchIDmatchTopics[au] = {}
        AuMatchIDmatchTopics[au][Id] = IDmatchTopics[Id]
        #if cc % 100000<=10: print AuMatchIDmatchTopics[au]


print len(AuMatchIDmatchTopics)
output = open(path + "AuMatchIDmatchTopics.dump","wb")
pickle.dump(AuMatchIDmatchTopics,output)

