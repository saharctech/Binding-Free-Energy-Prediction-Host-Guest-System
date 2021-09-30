#!/bin/bash
cd ../gb-outputs
for i in *.txt
do
	echo ${i%}
done
