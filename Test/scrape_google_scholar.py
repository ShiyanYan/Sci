import urllib2, urllib
import time
import re
import cPickle as pickle 

urlprefix = "http://scholar.google.com/citations?hl=en&view_op=search_authors&"
fin = open("tmp", "r")  # author list in dump 
fout = open("scholar.txt", "w")  #author list out txt
AuthorMatchDic = {}
#foutdump = open("../../ACMdata/authorMatch.dump","wb") # write out the mapping between author names and names+IDs

regaut = re.compile(r'<a class="cit-dark-large-link" href="\/citations.user=([^&]+)[^>]+>(.*?)<\/a>')
cc = 0
for line in fin:
	cc += 1

	line = line.strip()
	url = urlprefix + urllib.urlencode({"mauthors":line})
	res = urllib2.urlopen(url).read()
	matches = re.findall(regaut, res)
	if len(matches) == 0:
		if "didn't match any user profiles" in res:
			print line + "\t" + "not found"
			fout.write(line + "\t" + "not found\n")
		else:
			print line + "\t error!"
			fout.write(line + "\t error!\n")
	else:
		AuthorMatchDic[line] = {}
		print line
		fout.write(line)
		for match in matches:
			href = match[0]
			name = match[1]
			name = re.sub(r'<\/?strong>', '', name)
			print "\t" + name + "\t" + href
			fout.write("\t[" + name + "]\t" + href)
			AuthorMatchDic[line][name] = href
		fout.write("\n")
	time.sleep(1)

#pickle.dump(AuthorMatchDic,foutdump)