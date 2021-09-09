- Script folder contains the scripts used to prepare the files in respective folders with complex name.
- Complex.prmtop files in each folder is the dry complex including counterions
- dry-acd contains host acd dry molecule with no counterions because the host molecule almost has zero net charge.
- Guest.* files are guest related files including counterions. Net charge is zero
- prmtop and rst7 files in the current directory are the solvated complex molecules.

- Protocol used to prepare dry Host & Guest topology, coordinate and pdb files are as below:
---------------------------------------------------------------------------------------------------------
#CPPTRAJ is used to split rst7 and top files
#Complex cpptraj input file
parm ../complex_name.prmtop
trajin ../complex_name.rst7
strip :WAT outprefix complex
trajout complex.crd restart
trajout complex.pdb pdb
run
quit

#Host cpptraj input file
parm bcd-1-p.prmtop
trajin bcd-1-p.rst7
strip :WAT
strip :Cl-
strip :Na+
strip :MOL outprefix acd-host
trajout bcd-host.crd restart
trajout bcd-host.pdb pdb
run
quit

#Guest cpptraj input file
parm ../complex_name.prmtop
trajin ../complex_name.rst7
strip :WAT
strip :MGO outprefix guest_name
trajout guest_name.crd restart
trajout guest_name.pdb pdb
run
quit



