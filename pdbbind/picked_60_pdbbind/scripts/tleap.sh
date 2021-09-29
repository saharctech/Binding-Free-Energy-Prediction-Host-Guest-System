#!/bin/bash
for folder in ../picked-60/*; do
    cd "$folder"
    mkdir "top_crd"
    cd "top_crd"
    $AMBERHOME/bin/tleap -f ../../../scripts/tleap.in
    cd ../..
done
