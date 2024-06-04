import yaml
from pathlib import Path

# Read Paths Template
with open('notebooks/paths_temp.yml', 'r') as f:
    paths = yaml.safe_load(f)

# Get Directory name (should be different for each student)
dir_name = Path('./').absolute().parent.name

# Create empyt new dictionary for yaml file
new_paths = {}

# Copy old into new dict and replace {{USER}} with actual Username
for key, val in paths.items():
    if '{{USER}}' in val:
        new_val = val.replace('{{USER}}', dir_name)
    else:
        new_val = val
    new_paths[key] = new_val

# Safe new yaml file
with open('notebooks/paths.yml', 'w') as outfile:
    yaml.dump(data=new_paths, stream=outfile)

# Create Workingspace
directories = [new_paths['serialize'], new_paths['post'], new_paths['shapefiles']]

for d in directories:
    dir_path = Path(d).resolve()
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f'Made Directory: {dir_path}')
    else:
        print(f'Directory exists: {dir_path}')