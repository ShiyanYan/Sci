#bash code for clustering
DICT=../../DictForPaper/MergedDicGramsNoUni
WORKPATH=../LangProc/
OUTPUTPATH=../../ClusterResults/
#python ${WORKPATH}occurrencCount.py ${DICT} ${OUTPUTPATH}gramslist
#python ${WORKPATH}co-occurrenceDetection.py ${OUTPUTPATH}gramslist ${OUTPUTPATH}word-links ${OUTPUTPATH}dict
#python ${WORKPATH}SimMatriCalc.py ${OUTPUTPATH}

Rscript ../TopicExtract/apcluster.R ${OUTPUTPATH}sim