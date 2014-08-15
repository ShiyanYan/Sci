#MetricsCalc.sh
. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
PATHE2=../../$wordSpaceName/

cd ../Metrics-Calc/

python MetricsCalc.py $PATHE2 ../../ACMdata/ID_Metadata_Proc.txt
python MetricsCalc2.py $PATHE2
