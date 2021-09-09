#!/bin/bash


for file in ../*.prmtop
do
	complex_name=`basename $file .prmtop`
	sed -r "s/guest_name/guest-$complex_name/g;s/complex_name/$complex_name/g" cpptraj-guest.in > cpptraj-guest-new.in
	sed -r "s/host_name/host-$complex_name/g;s/complex_name/$complex_name/g" cpptraj-host.in > cpptraj-host-new.in
	sed -r "s/complex_name/$complex_name/g" cpptraj-com.in > cpptraj-com-new.in
	cd ..
	mkdir $complex_name
	cd $complex_name
	$AMBERHOME/bin/cpptraj -i ../scripts/cpptraj-guest-new.in
	$AMBERHOME/bin/cpptraj -i ../scripts/cpptraj-host-new.in
	$AMBERHOME/bin/cpptraj -i ../scripts/cpptraj-com-new.in

	mv complex.$complex_name.prmtop complex.prmtop
	mv guest-$complex_name.$complex_name.prmtop guest.prmtop
	mv guest-$complex_name.crd guest.crd
	
	mv host-$complex_name.$complex_name.prmtop host.prmtop
	mv host-$complex_name.crd host.crd
	mv complex.pdb $complex_name.pdb

	cp $complex_name.pdb ../../../mobley-dry-complex-pdb
	cd ../scripts
done
	
