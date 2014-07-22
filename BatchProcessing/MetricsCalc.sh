#MetricsCalc.sh
. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
PATHE2=../../$wordSpaceName/


cd ../SelfCitation/
MetricsCalc.py $PATHE2 ../../ACMdata/ID_Metadata_Proc.txt
MetricsCalc2.py $PATHE2