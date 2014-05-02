PATHE=../../ClusterResults/
head ${PATHE}similarityFile
head ${PATHE}pref.txt
cd ../apcluster/

./apcluster ${PATHE}similarityFile ${PATHE}pref.txt ${PATHE}apcluster/ 

