#!/bin/bash
#complex_names=()
#declare -p complex_names

while read line; do
	complex_names+=($line)
done < complex_names.txt



for i in ${complex_names[@]}
do
	cd ../$i
	#complex pbsa
	$AMBERHOME/bin/pbsa -i ../scripts/pbsa.in -p complex.prmtop -c complex.crd -o complex-pb.out
	tail -n 44 complex-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,16}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,20}' >> $i-pb.txt	
	
	#Guest pbsa
	$AMBERHOME/bin/pbsa -i ../scripts/pbsa.in -p guest.prmtop -c guest.crd -o guest-pb.out
	tail -n 40 guest-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,16}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,20}' >> $i-guest-pb.txt
	
	#Host pbsa
	$AMBERHOME/bin/pbsa -i ../scripts/pbsa.in -p host.prmtop -c host.crd -o host-pb.out
	tail -n 44 host-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,16}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,20}' >> $i-host-pb.txt

	#copy pbsa outputs to another folder
	cp $i-pb.txt ../../../sample5-pbsa-outputs
	cp $i-guest-pb.txt ../../../sample5-pbsa-outputs
	cp $i-host-pb.txt ../../../sample5-pbsa-outputs
	cd ../scripts
done



