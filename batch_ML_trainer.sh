#!/bin/bash

#SBATCH --nodes=1
#SBATCH --account=carbon-kp
#SBATCH --partition=carbon-kp
#SBATCH -o ./Slurm_Reports/slurm-%A_%a.out # STDOUTS

source activate CO2_Eddy

python ML_trainer.py


