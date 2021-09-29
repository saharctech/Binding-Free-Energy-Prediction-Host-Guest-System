#!/bin/bash
for folder in ../raw_data_test/*; do
    cd "$folder"
    mkdir "pbsa"
    cd "pbsa"
    #protein
    $AMBERHOME/bin/pbsa -i ../../../scripts/pbsa.in -p ../top_crd/pro.top -c ../top_crd/pro.crd -O -o pro-pb.out
    tail -n 44 pro-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,21}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,18}' >> pro-pb.txt
    #ligand
    $AMBERHOME/bin/pbsa -i ../../../scripts/pbsa.in -p ../top_crd/lig.top -c ../top_crd/lig.crd -O -o lig-pb.out
    tail -n 44 lig-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,21}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,18}' >> lig-pb.txt
    #complex
    $AMBERHOME/bin/pbsa -i ../../../scripts/pbsa.in -p ../top_crd/complex.top -c ../top_crd/complex.crd -O -o complex-pb.out
    tail -n 44 complex-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,21}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,18}' >> complex-pb.txt
    cd ../..
done
