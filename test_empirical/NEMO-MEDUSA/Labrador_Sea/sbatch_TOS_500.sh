#!/bin/bash
#SBATCH --job-name=TOS_500
#SBATCH --partition=standard
#SBATCH --account=nemo
#SBATCH --qos=standard
#SBATCH --time=24:00:00

/home/users/thopri/micromamba/envs/dew/bin/python /gws/nopw/j04/nemo_vol4/thopri/deep-early-warnings-pnas/test_empirical/NEMO-MEDUSA/Labrador_Sea/main.py --parameter TOS --five_hundred
