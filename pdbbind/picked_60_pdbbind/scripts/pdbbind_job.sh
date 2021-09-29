#!/bin/bash
#SBATCH --job-name="pdbbind60"
#SBATCH --output="pdbbind60.out"
#SBATCH --partition=compute
#SBATCH --nodes=4
#SBATCH --account=csu104
#SBATCH --ntasks-per-node=5
#SBATCH --export=ALL
#SBATCH --mem=248G
#SBATCH -t 03:00:00
module purge
module load slurm
module load cpu/0.15.4  gcc/9.2.0  openmpi/3.1.6
module load amber/20

bash lig_preparation.sh
bash tleap.sh
bash gbnsr6.sh
bash pbsa.sh
