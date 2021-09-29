#!/bin/bash
for folder in ../picked-60/*; do
    cd "$folder"
    mkdir "antechamber_files"
    cd "antechamber_files"
    $AMBERHOME/bin/antechamber -i ../lig_new.pqr -fi pdb -o lig.prep -fo prepi -c bcc
    $AMBERHOME/bin/parmchk2 -i lig.prep -f prepi -o lig.frcmod
    cd ../..
done
