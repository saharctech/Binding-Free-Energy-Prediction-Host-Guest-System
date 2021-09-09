- Script folder contains the scripts used to prepare the files in respective folders with complex name.
- Complex.prmtop files in each folder is the dry complex including counterions
- dry-acd contains host acd dry molecule with no counterions because the host molecule almost has zero net charge.
- Guest.* files are guest related files including counterions.
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
parm oa-3.prmtop
trajin oa-3.rst7
strip :WAT
strip :MOL
strip :10  outprefix acd-host
trajout host-oa.crd restart
trajout host-oa.pdb pdb
run
quit

#oa-7 and oa-8 does not work with this protocol. Left them alone.
#Guest cpptraj input file
parm ../complex_name.prmtop
trajin ../complex_name.rst7
strip :WAT
strip :OCT
strip :10
strip :9
strip :8
strip :7
strip :6
strip :5
strip :4
strip :3 outprefix guest_name
trajout guest_name.crd restart
trajout guest_name.pdb pdb
run
quit



