# Binding free energy prediction of Host-Guest system
## About project
The current aim of this project is predicting enthalpy part of protein-ligand binding affinity and the ultimate goal is to build a system that can predict binding free energy of protein-ligand complexes. Accurate and fast calculation of binding free energy of biomolecules is essential for early stages of drug discovery process. We decided to start with Host-guest system because this system contains small molecules that's easier to study and much faster to run physics models. As our work evolves, we will expand this research to broader range of molecule sizes. Details about the techniques and model will be published soon.
## Contents of this directory
This directory and it's subdirectories provides below content:
- structure and simulation input files for benchmark sets provided by Mobley's group. For more
Details about the cd-set1, cd-set2 and cdcc system, refer to Mobley GitHub page [1].
- Dry complex, host and guest structure and simulation files.
- Results: contains the dataset, experimental results[1][3], physics parameters and analysis of the dataset.
- cd-set1: contains structural files, Amber coordinate and topology files as well as pbsa and gbnsr6 output files for cd-set-1 dataset.
- cd-set2: contains structural files, Amber coordinate and topology files as well as pbsa and gbnsr6 output files for cd-set-2 dataset.
- gdcc-set1: contains structural files, Amber coordinate and topology files as well as pbsa and gbnsr6 output files for gdcc-set1 dataset.
- SAMPL5: contains structural files, Amber coordinate and topology files as well as pbsa and gbnsr6 output files for SAMPL5 dataset[2].
- model: contains PGNN (Physics guided neural network) and Data Driven model.
- Script folder contains cpptraj and gbnsr6 scripts. 
- Complex.prmtop/host.prmtop/guest.prmtop files in each folder are the dry structure files.
- Complex.crd/host.crd/guest.crd files in each folder are the dry complex structure.



## References:
1 - Mobley's lab: https://github.com/MobleyLab/benchmarksets
2- Drug Design Data Resource (SAMPL5): https://drugdesigndata.org/about/sampl5
2- SAMPL5 experimental results: https://link.springer.com/article/10.1007/s10822-016-9970-8/tables/1