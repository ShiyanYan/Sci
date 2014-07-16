. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}

PATHE=../../$workSpaceName/
mkdir ${PATHE}apcluster

head ${PATHE}similarityFile
head ${PATHE}pref.txt
cd ../apcluster/

./apcluster ${PATHE}similarityFile ${PATHE}pref.txt ${PATHE}apcluster/ 
cd ../TopicExtract
python TopicsShow.py ${PATHE}
