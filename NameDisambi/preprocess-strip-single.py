#!/usr/bin/env python
# encoding: utf-8
"""
preprocess-strip-single.py

Created by Theresa Velden on 2009-11-09.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import string
import pickle
from sets import Set


#extract data from AU field of ISI records
def findAU(line):
    # test whether line starts with AU
    if line[:2]=="AU":
       return 0
    else: 
        return 1       

def findmultipleAU(line):
    # test whether follow-up line of AU line is still part of AU field
    if line[:1]==" ": # adjust whitespace as required by input data file formatting
        return 0
    else:
        return 1

f1 = open("in_original.txt", "r")
f2 = open("in-normalized_stripped.txt", "w")

text = f1.readlines()
f1.close()

record=""
flag="green"

# LIST OF COAUTHOR TUPLES (1 tuple per article)

i=0 # counts all AU fields processed
score = 1
authors=[]
coauthorlist=[]

for line in text:
    if score==0:
        #check whether line is consecutive part of AU entry
        score=findmultipleAU(line)
        if score==0:
            authornumber+=1	
            authors.append(line[1:-1]) # adjust whitespace as required by input data file formatting
        else:
            if authornumber>1:	
                # polish (normalize) elements
                j=0
                while j < len(authors):
                    authors[j]=authors[j].rstrip("\n")
                    authors[j]=authors[j].lstrip()
                    authors[j]=authors[j].upper()
                    nameparts=authors[j].split(",")
                    surname=nameparts[0]
                    if " " in surname:
                        surname=surname.replace(" ", "")
                        print 'removing blank from surname', surname
                    if "-" in surname:
                        surname=surname.replace("-", "")
                        print 'removing hyphen from surname', surname
                    if len(nameparts)==1:
                        authors[j]=surname
                        print 'no initials', surname
                    else:
                        authors[j]=surname+","+nameparts[1]
                        if len(nameparts[1])>3:
                            print "more than 2 initials", authors[j]
                    if authors[j]=="":
                        del authors[j]
                        print "deleting empty author"
                    j=j+1
                record=record+"AU "+authors[0]+"\n"
                for index in range(1,len(authors)):
                    record=record+"   "+authors[index]+"\n"
                record=record+line
                score=1          
                continue
            else:
                print 'single author paper'
                flag="red"	                 
    else:
       score=findAU(line)
       if score==0:
          authors=[]
          i=i+1
          authors.append(line[3:-1]) #start author entry (anew)
       # test next line
       else:
          if line[:3]=="ID ":
             if flag=="green":	
                f2.write(record)
             flag="green"
             record=line
             authornumber=1 
          else:
             record=record+line	


f2.close()

