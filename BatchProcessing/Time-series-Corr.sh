# The code to produce the time-series and correlation .csv files for R
. ../parameter/global-parameter.txt
workSpaceName=../../${workSpaceName}/
metricsName=Entropy,Entropy2,Simpson,Gini,GLscore,Shiyan1,Shiyan2
cd ../Corr/

echo "Generate some temp files"
python GenerateAUIDmatchTopics.py ${workSpaceName}

echo "Calculate scores for authors"
python FinalScores.py ${workSpaceName}

echo "Begin integrating data"

python integrateData.py ${workSpaceName} ${metricsName}

echo "Correlation Files Done"

echo "Begin Time-series Generation"

cd ../Time-series/

echo "Norm 1"
python time-variation-average-N1.py ${workSpaceName} ${metricsName}

echo "Norm 2"
python time-variation-average-N2.py ${workSpaceName} ${metricsName}

echo "Done"
