#!/bin/bash
cd ../pb-outputs
for i in *.txt
do
	echo ${i%}
done
