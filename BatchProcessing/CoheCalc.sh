#Coherence Calculation

. ../parameter/global-parameter.txt
dicName=${dicName}
wordSpaceName=${workSpaceName}
PATHE2=../../$wordSpaceName/

python ../Temp-File-Generate/CluSimCalc.py $PATHE2


python ../Temp-File-Generate/CoherenceAveDis.py $PATHE2
python ../Temp-File-Generate/CoherenceCitation.py $PATHE2 ../../ACMdata/ID_RF.dump
python ../Temp-File-Generate/CoherenceCoauthor.py $PATHE2 ../../ACMdata/ID_AU_AF