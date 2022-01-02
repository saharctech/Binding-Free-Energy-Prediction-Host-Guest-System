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
            df = pd.DataFrame(lig_lines, columns=['effective-born-radii'])
            df.to_csv('complex_info.csv', index=True)
            # print(df)
        file_name = complex + '_info.csv'
        os.rename('complex_info.csv',file_name)
    except OSError as e:
        print(complex + " is not a valid file")
    os.chdir('../')






