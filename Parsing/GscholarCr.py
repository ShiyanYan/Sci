#google scholar crawling
import urllib2

req = urllib2.Request('http://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=M.+Ackeman')
response = urllib2.urlopen(req)
the_page = response.read()
print the_page