#!/bin/bash

#SBATCH --job-name=Berkland_Shock_2D
#SBATCH --nodes=8  # Increase number of nodes
#SBATCH --ntasks=32  # Increase parallelism
#SBATCH --mem-per-cpu=2GB  # More memory per core
#SBATCH --time=7-00:00:00  # 7 days
#SBATCH --partition=long
#SBATCH --error=/home1/mberkland2023/repos/smilei-pic/shock/2d/current_job/output_56GB_2-12-2025/error/testjob.%J.err
#SBATCH --output=/home1/mberkland2023/repos/smilei-pic/shock/2d/current_job/output_56GB_2-12-2025/output/testjob.%J.out

# Only load MPICH if needed
# module load mpich  # Remove this if ./run2d.sh does it

echo "Starting job at: $(date)"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is $(pwd)"

# Run the simulation
# Run the Smilei simulation with mpirun as root
num_procs=8  # Set the number of processes here
OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 mpirun -np $num_procs smilei shock_2d.py

echo "Hi mom!"
