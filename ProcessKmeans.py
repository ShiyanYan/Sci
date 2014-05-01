import pickle
dicts = pickle.load(open("../ACMdata/output/outdic","r"))

infile = open("../ACMdata/output/out3","r")
i = 0
clusters = {}
for line in infile:
    if line == "": break
    i += 1
    line = line[0:len(line)-1]
    c = int(line)
    if c in clusters:
        clusters[c].append(dicts[i])
    else:
        clusters[c] = []
        clusters[c].append(dicts[i])

print len(clusters)
outfile = open("../ACMdata/output/KmeansResults","w")
i = 0
for cc in clusters:
    i += 1
    outfile.write("---------------------------Words in Cluster " +str(i) + "-----------------------------------\n" )
    lis = clusters[cc]
    for tt in lis:
        outfile.write(tt+" || ")
    outfile.write("\n")

outfile.close()
