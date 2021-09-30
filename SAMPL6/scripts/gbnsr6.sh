#!/bin/bash
#complex_names=()
#declare -p complex_names
cd ../prmtop
for file in *
do
  cd $file/"top-crd"
	#complex gbnsr6
	$AMBERHOME/bin/gbnsr6 -i ../../../scripts/gbnsr6.in -p complex.prmtop -c complex.crd -o complex-gb.out
	tail -n 15 complex-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $file-gb.txt
	
	#Guest gbnsr6
	$AMBERHOME/bin/gbnsr6 -i ../../../scripts/gbnsr6.in -p guest.prmtop -c guest.crd -o guest-gb.out
	tail -n 15 guest-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $file-guest-gb.txt
	
	#Host gbnsr6
	$AMBERHOME/bin/gbnsr6 -i ../../../scripts/gbnsr6.in -p host.prmtop -c host.crd -o host-gb.out
	tail -n 15 host-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $file-host-gb.txt

	#copy gbnsr6 outputs to another folder
	cp $file-gb.txt ../../../gb-outputs
	cp $file-guest-gb.txt ../../../gb-outputs
	cp $file-host-gb.txt ../../../gb-outputs
	cd ../..
done


