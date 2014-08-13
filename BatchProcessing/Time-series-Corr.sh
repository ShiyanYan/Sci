# The code to produce the time-series and correlation .csv files for R
. ../parameter/global-parameter.txt
workSpaceName=../../${workSpaceName}/

cd ../Corr/

echo "Generate some temp files"
python GenerateAUIDmatchTopics.py ${workSpaceName}

echo "Calculate scores for authors"
python FinalScores.py ${workSpaceName}

echo "Begin integrating data"
<<<<<<< HEAD
python integrateData.py ${workSpaceName} Entropy,Entropy2,Simpson,Gini,GLscore,Shiyan1,Shiyan2
=======
python integrateData.py ${workSpaceName} Entropy,Entropy2,Simpson,Gini,GLscore,Shiyan1,Shiyan2,
>>>>>>> 2b88aee666bbdc92c1c26fd63478f283dca1392d
echo "Correlation Files Done"

echo "Begin Time-series Generation"

cd ../Time-series/

echo "Norm 1"
python time-variation-average-N1.py ${workSpaceName}

echo "Norm 2"
python time-variation-average-N2.py ${workSpaceName}

echo "Done"
