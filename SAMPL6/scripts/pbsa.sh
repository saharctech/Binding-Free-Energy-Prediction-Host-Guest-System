#!/bin/bash

cd ../prmtop
for file in *
do
  cd $file/"top-crd"
	#complex pbsa
	$AMBERHOME/bin/pbsa -i ../../../scripts/pbsa.in -p complex.prmtop -c complex.crd -o complex-pb.out
	tail -n 44 complex-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,16}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,20}' >> $file-pb.txt
	
	#Guest pbsa
	$AMBERHOME/bin/pbsa -i ../../../scripts/pbsa.in -p guest.prmtop -c guest.crd -o guest-pb.out
	tail -n 40 guest-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,16}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,20}' >> $file-guest-pb.txt
	
	#Host pbsa
	$AMBERHOME/bin/pbsa -i ../../../scripts/pbsa.in -p host.prmtop -c host.crd -o host-pb.out
	tail -n 44 host-pb.out | grep -E -o 'EPB.{0,21}|ECAVITY.{0,16}|EELEC.{0,20}|Etot.{0,20}|VDWAALS.{2,20}' >> $file-host-pb.txt

	#copy pbsa outputs to another folder
	cp $file-pb.txt ../../../pb-outputs
	cp $file-guest-pb.txt ../../../pb-outputs
	cp $file-host-pb.txt ../../../pb-outputs
	cd ../..
done



