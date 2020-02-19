#!/bin/bash

#SBATCH --nodes=1
#SBATCH --account=carbon-kp
#SBATCH --partition=carbon-kp

source activate CO2_Eddy

python SQL_download.py
