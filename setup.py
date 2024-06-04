import yaml
from pathlib import Path

# Read Paths Template
with open('notebooks/paths_temp.yml', 'r') as f:
    paths = yaml.safe_load(f)

# Get Directory name (should be different for each student)
dir_name = Path('./').absolute().name

# Create empyt new dictionary for yaml file
new_paths = {}

# Copy old into new dict and replace {{USER}} with actual Username
for key, val in paths.items():
    if '{{USER}}' in val:
        new_val = val.replace('{{USER}}', dir_name)
    new_paths[key] = new_val

# Safe new yaml file
with open('notebooks/paths.yml', 'w') as outfile:
    yaml.dump(data=new_paths, stream=outfile)