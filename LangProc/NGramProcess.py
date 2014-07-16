#N-gram Processing
import nltk
from nltk.corpus import *
import pickle
from nltk import bigrams
from nltk import trigrams
inputfile = open("../../ACMdata/in.txt","r") #Consider the batch processing later
punc_list = ['!','"','#','$','%','&','\\',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~']
stop_word = stopwords.words("english")
# Reading Papers
unigram_dict = {}
bigram_dict = {}
trigram_dict = {}
flag = False
TT = 0
NofBigram = {} #how many documents have these bigrams
NofTrigram = {} # how many documents have these trigrams
wholegrams = [] # the list of all the grams (unigram, bigram and trigram) 
infile1 = open("../../ACMdata/output/combinedDicNoisyVersion",'r')

#######
MergedDic = []
for t in infile1:
    MergedDic.append(t[0:len(t)-1])
MergedDic = sorted(MergedDic)
######
# MergedDic = pickle.load(infile1)
print "Begin Reading"
# read wiki dictionary
# infile2 = open("../../Wiki/wiki-titles",'r')
# i = 0
# WikiDic = []
# print "Begin Reading WikiDic"
# for line in infile2:
#     i += 1
#     if flag:
#         flag = False
#         continue
#     lens = len(line)
#     line = line[0:lens-1]
#     s = line.lower()
#     ss = s.replace("_"," ")
#     WikiDic.append(ss)
# print "End Reading WikiDic"

NofGram = {} # number of documents that have grams 
for line in inputfile:
    # if TT>4000: break
    if flag:
        flag = False
        TT += 1
        # print TT
        if (TT % 10000 == 0):
            print "Complete" + str(TT)
        abstr = line
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
        # POS = nltk.pos_tag(tokens)
        # POS_dict = {}
        # for ik in POS:
        #     if (ik[1]=="VB") or (ik[1]=="VBD") or (ik[1]=="VBG") or (ik[1]=="VBN") or (ik[1]=="VBP") or (ik[1]=="VBZ"):
        #         POS_dict[ik[0]] = 0
        #     else:
        #         POS_dict[ik[0]] = 1


        bigr = bigrams(tokens)
        trigr = trigrams(tokens)
        #print bigr
        flagt = []
        k = 0
        for unigg in tokens:
            if unigg in punc_list:
                continue
            if unigg in stop_word:
                continue
            gram = unigg
            if gram in flagt:
                k = k
            else:
                flagt.append(gram)
                if gram in NofGram:
                    NofGram[gram] +=1
                else:
                    NofGram[gram] = 1
            # if gram in unigram_dict:
            #     unigram_dict[gram] += 1
            # else:
            #     unigram_dict[gram] = 1
        #     if not (gram in WikiDic):
        #         continue
            # if gram in wholegrams:
            #     k = k
            # else:
            #     wholegrams.append(gram)

        for bigg in bigr:
            if (bigg[0] in punc_list) or (bigg[1] in punc_list):
                continue
            if (bigg[0] in stop_word) or (bigg[1] in stop_word):
                continue
            # if (POS_dict[bigg[0]]==0) or (POS_dict[bigg[1]]==0):
            #     continue
            # for j in range(0,2):
            #     lens = len(bigg[j])
            #     if (bigg[j][lens-1]=="."):
            #         bigg[j] = bigg[j][0:lens-2]
            gram = bigg[0] + " " + bigg[1]
            # if not (gram in WikiDic):
            #     continue
            # if gram in wholegrams:
            #     k = k
            # else:
            #     wholegrams.append(gram)
            if gram in flagt:
                k = k
            else:
                flagt.append(gram)
                if gram in NofGram:
                    NofGram[gram] +=1
                else:
                    NofGram[gram] = 1

            # if gram in bigram_dict:
            #     bigram_dict[gram] += 1
            # else:
            #     bigram_dict[gram] = 1
        # flagt = []
        for trigg in trigr:
            if (trigg[0] in punc_list) or (trigg[1] in punc_list) or (trigg[2] in punc_list):
                continue
            if (trigg[0] in stop_word) or (trigg[1] in stop_word) or (trigg[2] in stop_word):
                continue
            # if (POS_dict[trigg[0]]==0) or (POS_dict[trigg[1]]==0) or (POS_dict[trigg[2]]==0):
            #     continue  
            # for j in range(0,3):
            #     lens = len(trigg[j])
            #     if (trigg[j][lens-1]=="."):
            #         trigg[j] = trigg[j][0:lens-2]
            gram = trigg[0] + " " + trigg[1] + " " + trigg[2]
            # if not (gram in WikiDic):
            #     continue
            # if gram in wholegrams:
            #     k = k
            # else:
            #     wholegrams.append(gram)
            if gram in flagt:
                k = k
            else:
                flagt.append(gram)
                if gram in NofGram:
                    NofGram[gram] +=1
                else:
                    NofGram[gram] = 1
            # if gram in trigram_dict:
            #     trigram_dict[gram] += 1
            # else:
            #     trigram_dict[gram] = 1     

    if (line[0]=="A") and (line[1]=="B"):
        flag = True

print "Begin Writing"

# cc = 0
# outfile0 = open("../../ACMdata/grams/unigrams.txt","w")
# for w in sorted(unigram_dict):
#     if unigram_dict[w]<=10: continue
#     outfile0.write(str(w) + "\n")
# outfile0.close()

# outfile1 = open("../../ACMdata/grams/bigrams.txt","w")
# for w in sorted(bigram_dict):
#     if bigram_dict[w]<=5: continue
#     outfile1.write(str(w) + "\n")
# outfile1.close()

# outfile2 = open("../../ACMdata/grams/trigrams.txt","w")
# for w in sorted(trigram_dict):
#     if trigram_dict[w]<=5: continue
#     outfile2.write(str(w) + "\n")
# outfile2.close()

# outfile3 = open("../../ACMdata/NOBigram.txt","w")
# pickle.dump(NofBigram,outfile3)

# outfile3.close()

# outfile4 = open("../../ACMdata/NOTrigram.txt","w")
# # for w in sorted(NofTrigram,key=NofTrigram.get,reverse=True):
# #     cc += 1
# #     #if bigram_dict[w]<=5: break
# #     outfile4.write(str(w) + " " + str(NofTrigram[w]) + "\n")
# pickle.dump(NofTrigram,outfile4)
# outfile4.close()

# outfile5 = open("../../ACMdata/wholegrams","w")
# pickle.dump(wholegrams,outfile5)
# outfile5.close()

# outfile6 = open("../../ACMdata/showgrams","w")
# for t in wholegrams:
#     outfile6.write(t+"\n")
# outfile6.close()
print len(NofGram)
print "begin processing"
# NG = {}
# for t in NofGram:
#     i = 0
#     j = len(MergedDic)-1
#     f = False
#     while True:
#         if (i>=j): break
#         mid = (i+j)/2
#         if (t==MergedDic[mid]): f=True
#         if t<=MergedDic[mid]: 
#             j = mid
#         else:
#             i = mid + 1
#     if (t==MergedDic[i]): f = True
#     if f: 
#         NG[t] = NofGram[t]

# NofGram = NG

print "Begin Writing"
outfile7 = open("../../ACMdata/NofGram2","w")
pickle.dump(NofGram,outfile7)
outfile7.close()
i = 0
for t in NofGram:
    i +=1
    if (i>10): break
    print t,NofGram[t]

