#!/bin/bash
#complex_names=()
#declare -p complex_names

while read line; do
        complex_names+=($line)
done < complex_names.txt



for i in ${complex_names[@]}
do
	cd ../$i
        #copy gbnsr6 outputs to another folder
        cp $i-gb.txt ../../../mobley-gbnsr6-outputs
        cp $i-guest-gb.txt ../../../mobley-gbnsr6-outputs
        cp $i-host-gb.txt ../../../mobley-gbnsr6-outputs
        cd ../scripts
done
