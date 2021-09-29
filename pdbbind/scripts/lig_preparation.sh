#!/bin/bash
for folder in ../raw_data_test/*; do
    cd "$folder"
    mkdir "antechamber_files"
    cd "antechamber_files"
    $AMBERHOME/bin/pdb
    $AMBERHOME/bin/antechamber -i ../lig_new.pqr -fi pdb -o lig.prep -fo prepi -c bcc -at gaff -s 2
    $AMBERHOME/bin/parmchk2 -i lig.prep -f prepi -o lig.frcmod
    cd ../..
done