#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=civil-np
#SBATCH --partition=civil-np
#SBATCH -o ./Slurm_Reports/gridsearch-%A.out # STDOUTS

source activate CO2_Eddy

python gridsearch.py

