#!/bin/bash

cd ../prmtop
for file in *
do
#  sed -r "s/complex_name/$file/g" ../scripts/cpptraj-guest.in > ../scripts/cpptraj-guest-new.in
#  sed -r "s/complex_name/$file/g" ../scripts/cpptraj-host.in > ../scripts/cpptraj-host-new.in
#  sed -r "s/complex_name/$file/g" ../scripts/cpptraj-com.in > ../scripts/cpptraj-com-new.in
  cd $file
#  rm -r "top-crd"
#  cd ..
  mkdir "top-crd"
  cd "top-crd"
  $AMBERHOME/bin/cpptraj -i ../../../scripts/cpptraj-guest.in
  $AMBERHOME/bin/cpptraj -i ../../../scripts/cpptraj-host.in
  $AMBERHOME/bin/cpptraj -i ../../../scripts/cpptraj-com.in

  mv complex.complex.prmtop complex.prmtop
  mv guest.complex.prmtop guest.prmtop
  mv host.complex.prmtop host.prmtop
  mv complex.pdb $file.pdb
  cp $file.pdb ../../../sampl6-dry-complex-pdb
  cd ../..

done
	
