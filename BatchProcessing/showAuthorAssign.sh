. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
PATHE=../../$workSpaceName/
python ../SelfCitation/paperExtract.py Mark Newman ../../ACMdata/ID_Metadata_Proc.txt ${PATHE}
python ../SelfCitation/showPaperAssign.py ${PATHE} #> ${PATHE}AssignmentResults.txt

