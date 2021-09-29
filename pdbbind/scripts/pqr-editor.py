#read files from raw-data directory and remove WAT residues from the structural files
import os

path = "../raw-data"


folder_name = os.listdir(path)


#read each pqr file
for folder in folder_name:
    new_path = os.path.join(path, folder)
    if os.path.isdir(new_path):
        for file in os.listdir(new_path):
            if file == "com.pqr":
                # print("complex")
                #read complex pqr file
                com_pqr = open(os.path.join(new_path, file), "r")
                com_lines = com_pqr.readlines()
                com_pqr.close()
                ## delete the line with WAT keyword
                com_new = open(os.path.join(new_path, "com_new.pqr"), "w")
                for line in com_lines:
                    if "WAT" not in line:
                        com_new.write(line)
                com_new.close()
            if file == "pro.pqr":
                # print("Protein")
                #read protein pqr file
                pro_pqr = open(os.path.join(new_path, file), "r")
                pro_lines = pro_pqr.readlines()
                pro_pqr.close()
                ## delete the line with WAT keyword
                pro_new = open(os.path.join(new_path, "pro_new.pqr"), "w")
                for line in pro_lines:
                    if "WAT" not in line:
                        pro_new.write(line)
                pro_new.close()
            if file == "lig.pqr":
                # print("Ligand")
                #read ligand pqr file
                lig_pqr = open(os.path.join(new_path, file), "r")
                lig_lines = lig_pqr.readlines()
                lig_pqr.close()
                ## delete the line with WAT keyword
                lig_new = open(os.path.join(new_path, "lig_new.pqr"), "w")
                for line in lig_lines:
                    if "WAT" not in line:
                        lig_new.write(line)
                lig_new.close()
            # if file == ".DS_STORE":
            #     pass

