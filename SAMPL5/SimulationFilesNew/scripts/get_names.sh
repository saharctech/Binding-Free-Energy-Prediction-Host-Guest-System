#!/bin/bash
cd ..
for i in *.prmtop
do
	echo ${i%.*}
done
