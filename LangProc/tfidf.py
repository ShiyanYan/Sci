#tf*idf representation for every paper
import math
import pickle
import nltk
from nltk.corpus import *
from nltk import bigrams
from nltk import trigrams
punc_list = ['!','"','#','$','%','&','\\',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~']
stop_word = stopwords.words("english")

IdMatchScore = {}

inputfile = open("../../ACMdata/in.txt","r")
# inbigram = open("../../ACMdata/NOBigram.txt",'r')
# print "Begin Reading bigram frequency"
# bigramfrequency = pickle.load(inbigram)
# print "Begin Reading trigram frequency"
# intrigram = open("../../ACMdata/NOTrigram.txt",'r')
# trigramfrequency = pickle.load(intrigram)
ingrams = open("../../ACMdata/NofGram","r")
NofGram = {}
NofGram = pickle.load(ingrams)
NG = {}
for t in sorted(NofGram):
    if (t=="computer"): print "FLAG"
    NG[t] = NofGram[t]
NofGram = NG
ListofGram = []
i = 0
for t in NofGram:
    # i +=1
    # if i>10 : break
    # print t,NofGram[t]
    ListofGram.append(t)
ListofGram = sorted(ListofGram)
N = 150000.0
print "Begin Reading"
TT = 0
abflag = False
for line in inputfile:
    # if TT>400: break
    if abflag:
        TT +=1
        if (TT % 10000 == 0):
            print "Complete" + str(TT)
        abflag = False
        # process abstract
        gramcount = {}
        # bigramcount = {} # bigrams counts
        # trigramcount= {} # trigrams counts
        tokens = nltk.word_tokenize(line.lower())
        newtokens = []
        for too in tokens:
            newto = ""
            lens = len(too)
            if (too[lens-1]==".") and (lens>1):
                newto = too[0:lens-2]
            else:
                newto = too
            newtokens.append(newto)
        tokens=newtokens
        unigr = tokens
        bigr = bigrams(tokens)
        trigr = trigrams(tokens)
        for unigg in unigr:
            if unigg in punc_list: continue
            if unigg in stop_word: continue
            # if unigg=="computer": print "FLAG2"
            if unigg in gramcount:
                gramcount[unigg] += 1
            else:
                gramcount[unigg] = 1
        for bigg in bigr:
            if (bigg[0] in punc_list) or (bigg[1] in punc_list):
                continue
            if (bigg[0] in stop_word) or (bigg[1] in stop_word):
                continue
            gram = bigg[0] + " " + bigg[1]
            if gram in gramcount:
                gramcount[gram] +=1
            else:
                gramcount[gram] = 1
        for trigg in trigr:
            if (trigg[0] in punc_list) or (trigg[1] in punc_list) or (trigg[2] in punc_list):
                continue
            if (trigg[0] in stop_word) or (trigg[1] in stop_word) or (trigg[2] in stop_word):
                continue
            gram = trigg[0] + " " + trigg[1] + " " + trigg[2]
            if gram in gramcount:
                gramcount[gram] +=1
            else:
                gramcount[gram] = 1
        scoreMatch = {}
        for gram in gramcount:
            f = False
            i = 0
            j = len(ListofGram)-1
            while True:
                if (i>=j): break
                mid = (i+j)/2
                if (gram==ListofGram[mid]): f=True
                if gram<=ListofGram[mid]: 
                    j = mid
                else:
                    i = mid + 1
            # if (gram == "computer"): 
            #     print i,j,mid,str(f)
            if (gram==ListofGram[i]): f = True

            if f:
                score = gramcount[gram] * math.log(N/NofGram[gram])
                scoreMatch[gram] = score
        # for bigg in bigramcount:
        #     score = bigramcount[bigg] * math.log(N/bigramfrequency[bigg])
        #     word = bigg[0] + " " + bigg[1]
        #     scoreMatch[word] = score
        # for trigg in trigramcount:
        #     score = trigramcount[trigg] * math.log(N/trigramfrequency[trigg])
        #     word = trigg[0] + " " + trigg[1] + " " + trigg[2]
        #     scoreMatch[word] = score
        if (idnow != ""):
            IdMatchScore[idnow] = scoreMatch
            idnow=""

    if (line[0]=='I') and (line[1]=='D'):
        idnow = line[3:len(line)-1]
    if (line[0]=='A') and (line[1]=='B'):
        abflag = True
i = 0
for ids in IdMatchScore:
    i += 1
    if i>150:
        break
    writematch = IdMatchScore[ids]
    j = 0
    print str(i)
    for word in sorted(writematch,key=writematch.get,reverse=True):
        j += 1
        if (j>10):
            break
        print word,str(writematch[word])
print "Begin Writing"
outfile = open("../../ACMdata/IdMatchScore","w")
print len(IdMatchScore)
pickle.dump(IdMatchScore,outfile)
outfile.close()


