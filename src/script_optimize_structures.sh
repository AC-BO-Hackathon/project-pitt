#!/bin/bash

NUM_LAYERSS='2 4 6 8'
NUM_INIT=10
NUM_ITER=500

for NUM_LAYERS in $NUM_LAYERSS
do
    for SEED in $(seq 42 42 420)
    do
        echo $NUM_LAYERS $NUM_INIT $NUM_ITER $SEED

        sbatch slurm_optimize_structures.sh $NUM_LAYERS $NUM_INIT $NUM_ITER $SEED
        sleep 0.1s
    done
done
