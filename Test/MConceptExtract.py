#mother concept extract
import pickle
import struct
infile = open("../../Wiki/abbrvs.count","rb")

k = infile.read(1)
cc = 0
outfile = open("../../Wiki/abbrvs.count.out","wb")
for line in infile:
    s = ""
    s = line
    ss = s.split("	")
    if (len(ss)>1): outfile.write(ss[1][0:len(ss[1])])
    # outfile.write(s)
   # line = infile.read(1)
   # for t in line:
   #     print "t=",t
   #     k = struct.unpack('i',t)
   #     print k
    cc +=1
    # if cc>100: break
print cc
outfile.close()