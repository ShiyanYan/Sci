. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
PATHE=../../$workSpaceName/
python ../PaperAssignment/paperExtract.py Jon Kleinberg ../../ACMdata/ID_Metadata_Proc.txt ${PATHE}
python ../PaperAssignment/showPaperAssign.py ${PATHE} #> ${PATHE}AssignmentResults.txt

