#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=carbon-kp
#SBATCH --partition=carbon-kp

source activate CO2_Eddy

python gridsearch.py

