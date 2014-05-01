#!/bin/bash

# . ../parameters-disambiguate

cd ../../ACMdata/nameDis/

echo $(date): preprocessing - remove single authors >> log.txt

cp ../../Sci/NameDisambi/preprocess-strip-single.py .

python preprocess-strip-single.py

echo $(date): preprocessing - extract name redundancy file >> log.txt

cp ../../Sci/NameDisambi/extract-nameredundancy.py . 

python extract-nameredundancy.py

mkdir code-archive
mv *.py code-archive

echo $(date): disambiguating author names >> log.txt

mkdir disambiguation
mkdir disambiguation/input
mkdir disambiguation/output
mkdir disambiguation/code

$rundir=run1
cp ../../Sci/NameDisambi/disambiguate-final.pl disambiguation/code
cp NameRedundancies.txt disambiguation/input/names-redundancy_$rundir.txt
cp "in-normalized_stripped.txt" "disambiguation/input/"$rundir"_in-normalized_stripped.txt"
cd disambiguation/code
perl disambiguate-final.pl $rundir

# mv  ../../"in.txt" ../../in_original.txt
# mv ../output/"$rundir"_in-normalized_stripped-disambiguated.txt ../../"in_all-years.txt"

echo "DONE!"

