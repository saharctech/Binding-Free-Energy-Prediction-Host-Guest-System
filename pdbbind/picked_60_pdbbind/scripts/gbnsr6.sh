#!/bin/bash
for folder in ../picked-60/*; do
    cd "$folder"
    mkdir "gbnsr6"
    cd "gbnsr6"
    #protein
    $AMBERHOME/bin/gbnsr6 -i ../../../scripts/gbnsr6.in -p ../top_crd/pro.top -c ../top_crd/pro.crd -O -o pro-gb.out
    tail -n 15 pro-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> pro-gb.txt
    #ligand
    $AMBERHOME/bin/gbnsr6 -i ../../../scripts/gbnsr6.in -p ../top_crd/lig.top -c ../top_crd/lig.crd -O -o lig-gb.out
    tail -n 15 lig-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> lig-gb.txt
    #complex
    $AMBERHOME/bin/gbnsr6 -i ../../../scripts/gbnsr6.in -p ../top_crd/complex.top -c ../top_crd/complex.crd -O -o complex-gb.out
    tail -n 15 complex-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> complex-gb.txt
    cd ../..
done
