output_dir="output_56GB_2-19-2025"

# Move all files (not directories) except the specified ones to the output directory
shopt -s extglob
for file in *; do
  if [[ -f "$file" && "$file" != "shock_2d.py" && "$file" != "pp.py" && "$file" != "${0##*/}" && "$file" != *.sh ]]; then
    mv "$file" "$output_dir"
  fi
done

# Copy pp.py to the output directory
cp pp.py "$output_dir"
cp pp.sh "$output_dir"

# Unset the extglob shell option
shopt -u extglob

echo "Files moved to $output_dir."
