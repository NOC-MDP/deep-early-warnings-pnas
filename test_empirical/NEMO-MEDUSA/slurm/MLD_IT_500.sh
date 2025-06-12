#!/bin/bash
#SBATCH --job-name=TOS_IR_500
#SBATCH --partition=standard
#SBATCH --account=nemo
#SBATCH --qos=standard
#SBATCH --time=24:00:00

/home/users/thopri/micromamba/envs/dew/bin/python ../main.py --parameter TOS --region Irminger_Sea --five_hundred
