#!/bin/bash
#complex_names=()
#declare -p complex_names

while read line; do
        complex_names+=($line)
done < complex_names.txt



for i in ${complex_names[@]}
do
	cd ../$i
        #copy PBSA outputs to another folder
        cp $i-pb.txt ../../../mobley-pbsa-outputs/cd-set2
        cp $i-guest-pb.txt ../../../mobley-pbsa-outputs/cd-set2
        cp $i-host-pb.txt ../../../mobley-pbsa-outputs/cd-set2
        cd ../scripts
done
