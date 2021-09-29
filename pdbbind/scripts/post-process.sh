#!/bin/bash
cd ../picked_60_pdbbind/picked-60_2
for folder in *; do
    cd $folder
#    cd gbnsr6
#    mv complex-gb.txt $folder-complex-gb.txt
#    mv lig-gb.txt $folder-lig-gb.txt
#    mv pro-gb.txt $folder-pro-gb.txt
#    cp $folder-complex-gb.txt ../../../../gb_outputs
#    cp $folder-lig-gb.txt ../../../../gb_outputs
#    cp $folder-pro-gb.txt ../../../../gb_outputs
#    cd pbsa
##    mv complex-pb.txt $folder-complex-pb.txt
##    mv lig-pb.txt $folder-lig-pb.txt
##    mv pro-pb.txt $folder-pro-pb.txt
#    cp $folder-complex-pb.txt ../../../../pb_outputs
#    cp $folder-lig-pb.txt ../../../../pb_outputs
#    cp $folder-pro-pb.txt ../../../../pb_outputs
    cd top_crd
    mv complex.pdb $folder.pdb
    cp $folder.pdb ../../../../dry-pdb-complex
    cd ../..
done
