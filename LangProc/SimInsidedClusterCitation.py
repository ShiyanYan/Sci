#SimInsidedClusterCitation.py
import cPickle as pickle
import sys
import math
import operator
path = sys.argv[1]

IdMatchTopics = pickle.load(open(path + "IdMatchTopics","r"))
ID_RF = pickle.load(open(sys.argv[2],"r"))  # in ACMdata directory

output = open(path + "SimInsideCitation.txt","w")
outputdump = open(path + "SimInsideCitation.dump","w")

tot = {} # the number papers have the certain topic
score = {} # the score of every topic
cc  = 0
print cc
for Id in IdMatchTopics:
    if not Id in ID_RF: continue
    RFlist = ID_RF[Id]
    N = len(RFlist)
    tt = 0
    cc += 1
    print cc
    if cc % 10000==0: print "Proc" + str(cc) + "Finished"
    for topic0 in sorted(IdMatchTopics[Id],key=IdMatchTopics[Id].get,reverse=True):
        tt += 1
        if (tt>2) or (IdMatchTopics[Id][topic0]<0.3): break
        #s0 = IdMatchTopics[Id][topic0]
        if topic0 in tot:
            tot[topic0] += 1
        else:
            tot[topic0] = 1
        for RFID in RFlist:
            if not RFID in IdMatchTopics: continue
            if topic0 in IdMatchTopics[RFID]:
                if topic0 in score:
                    score[topic0] += (1 / float(N)) * float(IdMatchTopics[RFID][topic0])
                else:
                    score[topic0] = (1 / float(N)) * float(IdMatchTopics[RFID][topic0])

for topic in score:
    score[topic] = score[topic] / tot[topic]

pickle.dump(score,outputdump)

for topic in sorted(score,key=score.get,reverse=True):
    output.write(str(topic) + "\t" + str(score[topic]) + "\n")
