#!/bin/bash
cd pdbbind-refined-set/small-set-for-ali
for file in *.pdb;do
  complex_name=`basename $file .pdb`
  mkdir $complex_name
  cd $complex_name
  pdb4amber -i ../$file -o $complex_name.pdb
  cp $complex_name.pdb ../fixed-pdb
  cd ..
  rm -r $complex_name
done
