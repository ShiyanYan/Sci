#ABFTprocessing process the Ab and fulltext as a list of word from our dictionary
import nltk
import cPickle as pickle
import sys
dic = [] # the dic of grams
with open(sys.argv[1],"r") as f:
    for line in f:
        line = line[0:len(line)-1]
        dic.append(line)
dic = sorted(dic)
def isInDic(term):
    i = 0
    j = len(dic)-1
    while True:
        if i>=j: break
        mid = (i+j) / 2
        if dic[mid] == term: return True
        if term <= dic[mid]:
            j = mid
        else:
            i = mid + 1
    if mid>len(dic)-1: return False
    if dic[mid] == term: 
        return True
    else:
        return False
    
path = sys.argv[2]
AbMatchGrams = {} # abbrev match grams 
WholeMatchAb = {} # whole words + abbr  match abbr
inwholedic = open(path+"WholeMatchAb","rb")
WholeMatchAb = pickle.load(inwholedic)
listOfWhole = []
for t in WholeMatchAb:
    listOfWhole.append(t)
listOfWhole = sorted(listOfWhole)
listOfAb = []
for t in listOfWhole:
    listOfAb.append(WholeMatchAb[t])
print len(listOfWhole),len(listOfAb)
def Abbr(term):
    i = 0
    j = len(listOfWhole)-1
    while True:
        if i>=j: break
        mid = (i+j) / 2
        if (mid<0) or (mid>len(listOfWhole)-1):
            print mid,i,j
        if listOfWhole[mid] == term: return listOfAb[mid]
        if term <= listOfWhole[mid]:
            j = mid
        else:
            i = mid + 1
    if mid>len(listOfWhole)-1: return ""
    if listOfWhole[mid] == term: 
        return listOfAb[mid]
    else:
        return ""
# need new indexing
# Three functions of binary search



infile = open(sys.argv[3],"rb") #some simple version here
flaga = False
flagf = False
out = open(sys.argv[2]+"Paper_Assignment_Result.txt","wb") # some simple output
for line in infile:
    if (line[0:2] =="ID"):
        IDnow = line[3:len(line)-1]
        out.write(line)
    if flaga:
        wordlist = []
        flaga = False
        tokens = nltk.word_tokenize(line)
        newtokens = []
        INlist = []
        for too in tokens:
            newto = ""
            lens = len(too)
            if (too[lens-1]==".") and (lens>1):
                newto = too[0:lens-2]
            else:
                newto = too
            if newto==newto.upper(): INlist.append(newto)  # save the abbreviations
            newtokens.append(newto)
        tokens=newtokens  # solve the problem of "."
        leng = len(tokens)
        dicAbb = []
        trans = {}
        for i in range(0,leng):
            if i<leng-1: 
            	gram = tokens[i].lower() + " " + tokens[i+1].lower()
            	if isInDic(gram): 
            	    wordlist.append(gram)
            if i<leng-2:
                gram = tokens[i].lower() + " " + tokens[i+1].lower() + " " + tokens[i+2].lower()
                if isInDic(gram):
                	wordlist.append(gram)
                if Abbr(gram)!="":
                    abb = Abbr(gram)
                    dicAbb.append(abb)
                    if tokens[i].lower()==abb:
                        trans[abb] = tokens[i+1].lower() + tokens[i+2].lower()
                    else:
                        trans[abb] = tokens[i].lower() + tokens[i+1].lower()
            if i<leng-3:
                gram = tokens[i].lower() + " " + tokens[i+1].lower() + " " + tokens[i+2].lower() + " "+ tokens[i+3].lower()
                if Abbr(gram)!="":
                    abb = Abbr(gram)
                    dicAbb.append(abb)
                    if tokens[i].lower()==abb:
                        trans[abb] = tokens[i+1].lower() + tokens[i+2].lower() + tokens[i+3].lower()
                    else:
                        trans[abb] = tokens[i].lower() + tokens[i+1].lower() + tokens[i+2].lower()
        for gram in INlist:
            if gram.lower() in trans: wordlist.append(trans[gram.lower()])
        out.write("AB \n")
        for gram in wordlist:
            out.write(gram + "\t")
        out.write("\n")
    if (flagf) and (line!="\n"): ss = ss + line[0:len(line)-1]
    if (flagf) and (line=="\n"):
        #print ss
        wordlist = []
        flagf = False
        tokens = nltk.word_tokenize(ss)
        newtokens = []
        INlist = []
        for too in tokens:
            newto = ""
            lens = len(too)
            if (too[lens-1]==".") and (lens>1):
                newto = too[0:lens-2]
            else:
                newto = too
            if newto==newto.upper(): INlist.append(newto)  # save the abbreviations
            newtokens.append(newto)
        tokens=newtokens  # solve the problem of "."
        leng = len(tokens)
        dicAbb = []
        trans = {}
        for i in range(0,leng):
            if i<leng-1: 
            	gram = tokens[i].lower() + " " + tokens[i+1].lower()
            	if isInDic(gram): 
            	    wordlist.append(gram)
            if i<leng-2:
                gram = tokens[i].lower() + " " + tokens[i+1].lower() + " " + tokens[i+2].lower()
                if isInDic(gram):
                	wordlist.append(gram)
                if Abbr(gram)!="":
                    abb = Abbr(gram)
                    dicAbb.append(abb)
                    if tokens[i].lower()==abb:
                        trans[abb] = tokens[i+1].lower() + tokens[i+2].lower()
                    else:
                        trans[abb] = tokens[i].lower() + tokens[i+1].lower()
            if i<leng-3:
                gram = tokens[i].lower() + " " + tokens[i+1].lower() + " " + tokens[i+2].lower() + " "+ tokens[i+3].lower()
                if Abbr(gram)!="":
                    abb = Abbr(gram)
                    dicAbb.append(abb)
                    if tokens[i].lower()==abb:
                        trans[abb] = tokens[i+1].lower() + tokens[i+2].lower() + tokens[i+3].lower()
                    else:
                        trans[abb] = tokens[i].lower() + tokens[i+1].lower() + tokens[i+2].lower()
        for gram in INlist:
            if gram.lower() in trans: wordlist.append(trans[gram.lower()])
        out.write("FT \n")
        for gram in wordlist:
            out.write(gram + "\t")
        out.write("\n")
        out.write("\n")






    if (line[0]=="A") and (line[1]=="B"):
        flaga = True
    if (line[0]=="F") and (line[1]=="T"):
        flagf = True
        ss = ""
