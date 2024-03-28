#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cluster=smp
#SBATCH --partition=smp
#SBATCH --constraint=intel
#SBATCH --time=144:00:00
#SBATCH --qos=long
#SBATCH --mail-user=juk139@pitt.edu
#SBATCH --mail-type=TIME_LIMIT
#SBATCH --job-name=optimize-structures
#SBATCH -o ../outputs/output.%j.out


source ../script_prerun.sh

NUM_LAYERS=$1
NUM_INIT=$2
NUM_ITER=$3
SEED=$4

echo $NUM_LAYERS $NUM_INIT $NUM_ITER $SEED

python optimize_structures.py --num_layers $NUM_LAYERS --num_init $NUM_INIT --num_iter $NUM_ITER --seed $SEED

echo $''
crc-job-stats
