#!/bin/bash
cd PDB
for file in *.pdb ;do
  complex_name=`basename $file .pdb`
  mv $complex_name.pdb $complex_name-ligand.pdb
done