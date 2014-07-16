# bash codes for paper assignment
. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
cd ../PaperAssignment
PATHE=../../DictForPaper/
PATHE2=../../$wordSpaceName/
python AbbrevDetect.py ${PATHE}$dicName ${PATHE} ${PATHE2}
python AbFtProcessing.py ${PATHE}$dicName ${PATHE2} ../../ACMdata/ID_AB_FT.txt 
python PaperAssign.py ${PATHE2}
