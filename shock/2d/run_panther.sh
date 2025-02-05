#!/bin/bash

# Set the output directory name with the current date and time
output_dir=$(date +"%Y-%m-%d_%H-%M-%S")
echo "Output directory: $output_dir"

# Create the output directory
mkdir "$output_dir"

# Run panther_job.sh
chmod a+x ./panther_job.sh
/usr/bin/sbatch ./panther_job.sh

# Move all files (not directories) except the specified ones to the output directory
shopt -s extglob
for file in *; do
  if [[ -f "$file" && "$file" != "shock_2d.py" && "$file" != "pp.py" && "$file" != "${0##*/}" && "$file" != "panther_job.sh" && "$file" != "run2d.sh" ]]; then
    mv "$file" "$output_dir"
  fi
done

# Copy pp.py to the output directory
cp pp.py "$output_dir"

# Unset the extglob shell option
shopt -u extglob

echo "Files moved to $output_dir, simulation completed."