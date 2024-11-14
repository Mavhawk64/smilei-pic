#!/bin/bash

# Set the output directory name with the current date and time
output_dir=$(date +"%Y-%m-%d_%H-%M-%S")
echo "Output directory: $output_dir"

# Create the output directory
mkdir "$output_dir"

# Run the Smilei simulation with mpirun as root
num_procs=4  # Set the number of processes here
OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 mpirun -np $num_procs smilei shock_2d.py

# Move all files (not directories) except the specified ones to the output directory
shopt -s extglob
for file in *; do
  if [[ -f "$file" && "$file" != "shock_2d.py" && "$file" != "pp.py" && "$file" != "${0##*/}" ]]; then
    mv "$file" "$output_dir"
  fi
done

# Copy pp.py to the output directory
cp pp.py "$output_dir"

# Unset the extglob shell option
shopt -u extglob

echo "Files moved to $output_dir, simulation completed."
