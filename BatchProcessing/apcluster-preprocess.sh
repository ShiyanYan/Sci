#bash code for clustering
. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}

DICT=../../DictForPaper/$dicName
WORKPATH=../LangProc/
OUTPUTPATH=../../$wordSpaceName/
mkdir ${OUTPUTPATH}
python ${WORKPATH}occurrencCount.py ${DICT} ${OUTPUTPATH}gramslist
python ${WORKPATH}co-occurrenceDetection.py ${OUTPUTPATH}gramslist ${OUTPUTPATH}word-links ${OUTPUTPATH}dict
python ${WORKPATH}SimMatriCalc.py ${OUTPUTPATH}

#Rscript ../TopicExtract/apcluster.R ${OUTPUTPATH}sim
