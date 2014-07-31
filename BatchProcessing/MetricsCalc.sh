#MetricsCalc.sh
. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
PATHE2=../../$wordSpaceName/
#python ../LangProc/CluSimCalc.py ${workSpaceName}/
#python ../LangProc/SimInsidedCluster.py $PATHE2
python ../LangProc/SimInsidedCluster.py $PATHE2 ../../ACMdata/ID_RF.dump

#cd ../SelfCitation/

#python MetricsCalc.py $PATHE2 ../../ACMdata/ID_Metadata_Proc.txt
#python MetricsCalc2.py $PATHE2
