#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=carbon-kp
#SBATCH --partition=carbon-kp
#SBATCH -o ./Slurm_Reports/gridsearch-%A_%a.out # STDOUTS

source activate CO2_Eddy

python gridsearch.py

