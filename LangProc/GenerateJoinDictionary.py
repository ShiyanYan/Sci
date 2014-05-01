#GenerateJoinDictionary
import pickle
import nltk
# infile1 = open("../../ACMdata/MergeDic",'r')
# CorpusDic = pickle.load(infile1)

infile2 = open("../../Wiki/wiki-titles-sorted",'r')

unigram_dict = []
bigram_dict = []
trigram_dict = []
infileuni  = open("../../ACMdata/grams/unigrams.txt","r")
for t in infileuni:
    unigram_dict.append(t[0:len(t)-1])

infilebi = open("../../ACMdata/grams/bigrams.txt","r")
for t in infilebi:
    bigram_dict.append(t[0:len(t)-1])

infiletri = open("../../ACMdata/grams/trigrams.txt","r")
for t in infiletri:
    trigram_dict.append(t[0:len(t)-1])
unigram_dict = sorted(unigram_dict)
bigram_dict = sorted(bigram_dict)
trigram_dict = sorted(trigram_dict)

MergedDic = []
flag = True
i1 = 0
i2 = 0
i3 = 0
i = 0
print "begin matching"
for line in infile2:
    i += 1
    if (i % 1000000==0):
        print "Complete"+str(i)
    if flag:
        flag = False
        continue
    lens = len(line)
    line = line[0:lens-1]
    s = line.lower()
    s = s.replace("_"," ")
    if (s=="computer"): 
        print i
        print "------------------------"
        print s
        print unigram_dict[i1]
        print bigram_dict[i2]
        print trigram_dict[i3]
        # print unigram_dict[i1-1]
        # print bigram_dict[i2-1]
        # print trigram_dict[i3-1]
        print "-------------------------"
    while ((i1<len(unigram_dict)) and (unigram_dict[i1]<=s)):
        if (s==unigram_dict[i1]):
            if s=="computer": print "FLAG"
            MergedDic.append(s)
        i1 += 1
    while ((i2<len(bigram_dict)) and (bigram_dict[i2]<=s)):
        if (s==bigram_dict[i2]):
            MergedDic.append(s)
        i2 += 1
    while ((i3<len(trigram_dict)) and (trigram_dict[i3]<=s)):
        # if (s=="support vector machine"):
        #     print trigram_dict[i3]
        if (s==trigram_dict[i3]):
            MergedDic.append(s)
        i3 +=1

outfile = open("../../ACMdata/MergedDic","w")
pickle.dump(MergedDic,outfile)
outfile.close()

outfile2 = open("../../ACMdata/MergedDicGrams","w")
for t in MergedDic:
    outfile2.write(t+"\n")
outfile2.close()

