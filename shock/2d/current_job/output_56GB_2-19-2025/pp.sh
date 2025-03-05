#!/bin/bash

#SBATCH --job-name=Berkland_Shock_2D_PP
#SBATCH --nodes=1  # Use a single node to prevent file access conflicts
#SBATCH --ntasks=1  # Run only one process
#SBATCH --cpus-per-task=16  # Use multiple threads for performance
#SBATCH --mem=128G  # Allocate more memory
#SBATCH --time=7-00:00:00  # 7 days
#SBATCH --partition=long
#SBATCH --error=/home1/mberkland2023/repos/smilei-pic/shock/2d/current_job/output_56GB_2-19-2025/error/testjob_pp.%J.err
#SBATCH --output=/home1/mberkland2023/repos/smilei-pic/shock/2d/current_job/output_56GB_2-19-2025/output/testjob_pp.%J.out

echo "Starting job at: $(date)"
echo "Running on host: $(hostname)"
echo "Using $SLURM_CPUS_PER_TASK CPU cores."
echo "Current working directory is $(pwd)"

# Use environment variables to set thread limits (in case Python libraries use parallelism)
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OPENBLAS_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Run the post-processing script
python pp.py

echo "Done with Post Processing!"
