#!/bin/bash
for folder in ../raw_data_test/*; do
    cd "$folder"
    mkdir "top_crd"
    cd "top_crd"
    $AMBERHOME/bin/tleap -f ../../../scripts/tleap.in
    cd ../..
done
