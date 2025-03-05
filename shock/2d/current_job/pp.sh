#!/bin/bash

#SBATCH --job-name=Berkland_Shock_2D
#SBATCH --nodes=8  # Increase number of nodes
#SBATCH --ntasks=32  # Increase parallelism
#SBATCH --mem-per-cpu=2GB  # More memory per core
#SBATCH --time=7-00:00:00  # 7 days
#SBATCH --partition=long
#SBATCH --error=/home1/mberkland2023/repos/smilei-pic/shock/2d/current_job/output_56GB_2-19-2025/error/testjob_pp.%J.err
#SBATCH --output=/home1/mberkland2023/repos/smilei-pic/shock/2d/current_job/output_56GB_2-19-2025/output/testjob_pp.%J.out

echo "Starting job at: $(date)"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is $(pwd)"

# Run the simulation
python pp.py

echo "Done with Post Processing!"