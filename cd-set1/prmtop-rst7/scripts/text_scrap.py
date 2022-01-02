import os
import pandas as pd

path = "../../prmtop-rst7/scripts"
os.chdir(path)

# print(os.listdir())
with open("complex_names.txt", "r") as complex_file:
    complex_name = (complex_file.readlines())
    # print(complex_name)

for complex in range(len(complex_name)):
    complex_name[complex] = complex_name[complex].strip('\n')
os.chdir('..')
# print(os.listdir())
for complex in complex_name:
    lig_lines = []
    clean_text = []
    os.chdir(complex)
    os.listdir()
    # lig_gb_name = complex + "-guest-gb-radii.out"
    try:
        with open('complex-gb-radii.out', 'r') as file:
            lig_lines = [line.strip('\n') for line in file if "rinv" in line]
            for line in range(len(lig_lines)):
                lig_lines[line] = lig_lines[line].lstrip('rinv')
                lig_lines[line] = lig_lines[line].lstrip()
                lig_lines[line] = lig_lines[line][10:]
                lig_lines[line] = lig_lines[line].lstrip()
            print(lig_lines)
            atomic_radii_df = pd.DataFrame(lig_lines, columns=['effective-born-radii'])
            print(atomic_radii_df)

        # read complex coordinates
        pdb_file = complex + ".pdb"
        with open(pdb_file, 'r') as pdb_file:
            pdb_lines = [line.strip('\n') for line in pdb_file if "ATOM" in line]
            for line in range(len(pdb_lines)):
                pdb_lines[line] = pdb_lines[line][30:-3]
                pdb_lines[line] = pdb_lines[line].rstrip()
                pdb_lines[line] = pdb_lines[line].split(' ')
                pdb_lines[line] = [i for i in pdb_lines[line] if i != '']
            xyz_df = pd.DataFrame(pdb_lines, columns=['x', 'y', 'z', 'atomic-charge', 'atomic-radius'])
            print(xyz_df)
            # print(pdb_lines)
        final_df = pd.concat([xyz_df, atomic_radii_df], axis=1)
        print(final_df)
        final_df.to_csv('complex_info.csv', index=True)
        file_name = complex + '-info.csv'
        os.rename('complex_info.csv', file_name)
    except OSError as e:
        print(complex + " is not a valid file")
    os.chdir('../')






