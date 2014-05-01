#N-gram Processing
import nltk
from nltk.corpus import *
import pickle
from nltk import bigrams
from nltk import trigrams

dicFile = open("../../DictForPaper/CategoryTermsSorted","r")
dic = []
for line in dicFile:
    line = line[0:len(line)-1]
    dic.append(line)
dic = sorted(dic)

inputfile = open("../../ACMdata/in.txt","r") #Consider the batch processing later
punc_list = ['!','"','#','$','%','&','\\',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~']
stop_word = stopwords.words("english")

outfile = open("../../ACMdata/output/gramslist_Uni","w")

def inDic(term):
    i = 0
    j = len(dic)
    while True:
        if i>=j: break
        mid = (i+j) / 2
        if dic[mid] == term: return True
        if term <= dic[mid]:
            j = mid
        else:
            i = mid + 1
    if dic[mid] == term: 
        return True
    else:
        return False

print "Begin Reading"
flag = False
TT = 0
for line in inputfile:
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
        bigr = bigrams(tokens)
        trigr = trigrams(tokens)
        ss = []
        for unigg in tokens:
            if unigg in punc_list:
                continue
            if unigg in stop_word:
                continue
            gram = unigg
            if not (inDic(gram)): continue
            ss.append(gram)

        for bigg in bigr:
            if (bigg[0] in punc_list) or (bigg[1] in punc_list):
                continue
            if (bigg[0] in stop_word) or (bigg[1] in stop_word):
                continue
            gram = bigg[0] + " " + bigg[1]
            if not (inDic(gram)): continue
            ss.append(gram)

        for trigg in trigr:
            if (trigg[0] in punc_list) or (trigg[1] in punc_list) or (trigg[2] in punc_list):
                continue
            if (trigg[0] in stop_word) or (trigg[1] in stop_word) or (trigg[2] in stop_word):
            	continue
            gram = trigg[0] + " " + trigg[1] + " " + trigg[2]
            if not (inDic(gram)): continue
            ss.append(gram)     
        ss = sorted(ss)
        prev = ""
        for t in ss:
            if t!=prev:
                outfile.write(t+"\t")
                prev = t
        outfile.write("\n")                 


    if (line[0]=="A") and (line[1]=="B"):
        flag = True

outfile.close()