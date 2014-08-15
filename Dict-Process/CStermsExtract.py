#BFS for Wiki
path = "../../Wiki/Category/"
startterm = "computer science"
finallist = []
templist = []
newtemplist = []
finallist.append(startterm)
templist.append(startterm)

def isInFinallist(term):
    i = 0
    j = len(finallist)
    while True:
        if i>=j: break
        mid = (i+j) / 2
        if finallist[mid] == term: return True
        if term <= finallist[mid]:
            j = mid
        else:
            i = mid + 1
    if finallist[mid] == term: 
        return True
    else:
        return False

def isInTemplist(term):
    i = 0
    j = len(templist)
    while True:
        if i>=j: break
        mid = (i+j) / 2
        if templist[mid] == term: return True
        if term <= templist[mid]:
            j = mid
        else:
            i = mid + 1
    if templist[mid] == term: 
        return True
    else:
        return False

flag = True
iteration = 0
# Not certain if it is a DAG, need sort the previous one || left: should be in the templist, right should not be in finallist
while flag:
    iteration += 1
    flag = False
    infile = open(path + "categorylinks","rb")
    lastterm = ""
    lasttermflag = False  # judge whether the term now is in the category tree
    newtemplist = []
    for line in infile:
        ss = line.split("\t")
        ss[1] = ss[1][0:len(ss[1])-1]
        if ss[1]!=lastterm:
            lasttermflag = False
            lastterm = ss[1]
        if lasttermflag: continue
        if isInFinallist(lastterm):
            lasttermflag = True
            continue
        if not isInTemplist(ss[0]): continue
        flag = True
        newtemplist.append(ss[1])
        lasttermflag = True
    print "Iteration " + str(iteration) + " Complete. There are " + str(len(newtemplist)) + " categories added.\n"
    for t in newtemplist:
        finallist.append(t)
    finallist = sorted(finallist)
    templist = newtemplist
    templist = sorted(templist)
    infile.close()

print "There are " + str(len(finallist)) + " categories belong to Category: " + str(startterm) + "\n"
i = 0
outfile = open(path + "CategoryTerms","wb")
for t in finallist:
    outfile.write(t+"\n")
outfile.close()


        


