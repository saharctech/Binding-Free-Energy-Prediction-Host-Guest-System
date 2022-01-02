#!/bin/bash
#complex_names=()
#declare -p complex_names

while read line; do
	complex_names+=($line)
done < complex_names.txt

for i in ${complex_names[@]}
do
	cd ../$i
	#complex gbnsr6
#	$AMBERHOME/bin/gbnsr6 -i ../scripts/gbnsr6.in -p complex.prmtop -c complex.crd -o complex-gb.out
#	tail -n 15 complex-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $i-gb.txt
	$AMBERHOME/bin/gbnsr6 -i ../scripts/gbnsr6.in -p complex.prmtop -c complex.crd -O -o complex-gb-radii.out
	tail -n 15 complex-gb-radii.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $i-gb-radii.txt

	#Guest gbnsr6
#	$AMBERHOME/bin/gbnsr6 -i ../scripts/gbnsr6.in -p guest.prmtop -c guest.crd -o guest-gb.out
#	tail -n 15 guest-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $i-guest-gb.txt
	$AMBERHOME/bin/gbnsr6 -i ../scripts/gbnsr6.in -p guest.prmtop -c guest.crd -O -o guest-gb-radii.out
	tail -n 15 guest-gb-radii.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $i-guest-gb-radii.txt

	#Host gbnsr6
#	$AMBERHOME/bin/gbnsr6 -i ../scripts/gbnsr6.in -p host.prmtop -c host.crd -o host-gb.out
#	tail -n 15 host-gb.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $i-host-gb.txt
	$AMBERHOME/bin/gbnsr6 -i ../scripts/gbnsr6.in -p host.prmtop -c host.crd -O -o host-gb-radii.out
	tail -n 15 host-gb-radii.out | grep -E -o 'EGB.{0,21}|ESURF.{0,21}|EELEC.{0,20}|Etot.{0,20}|1-4 EEL.{2,18}' >> $i-host-gb-radii.txt

	#copy gbnsr6 outputs to another folder
#	cp $i-gb-radii.txt ../../../mobley-gbnsr6-outputs
#	cp $i-guest-gb-radii.txt ../../../mobley-gbnsr6-outputs
#	cp $i-host-gb-radii.txt ../../../mobley-gbnsr6-outputs
  cp $i-gb-radii.txt ../../gb_outputs
	cp $i-guest-gb-radii.txt ../../gb_outputs
	cp $i-host-gb-radii.txt ../../gb_outputs
	cd ../scripts
done


