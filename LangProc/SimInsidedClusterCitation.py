#SimInsidedClusterCitation.py
import cPickle as pickle
import sys
import math
path = sys.argv[1]

IdMatchTopics = pickle.load(open(path + "IdMatchTopics","r"))
ID_RF = sys.argv[2]  # in ACMdata directory

output = open(path + "SimInsideCitation.txt","w")
outputdump = open(path + "SimInsideCitation.dump","w")

tot = {} # the number papers have the certain topic
score = {} # the score of every topic

for Id in IdMatchTopics:
    if not Id in ID_RF: continue
    RFlist = ID_RF[Id]
    N = len(RFlist)
    tt = 0
    for topic0 in sorted(IdMatchTopics[Id],IdMatchTopics[Id].get,reverse=True):
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

for topic in score:
    output.write(str(topic) + "\t" + str(score[topic]) + "\n")