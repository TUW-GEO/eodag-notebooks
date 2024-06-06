import yaml
import getpass
from pathlib import Path

def make_subdirs():
    with open('notebooks/paths_temp.yml', 'r') as f:
        paths_template = yaml.safe_load(f)

    cwd = Path.cwd()

    paths = {}
    for key, val in paths_template.items():
        if 'USERDIR' in val:
            new_val = val.replace('USERDIR', str(cwd))
        else:
            new_val = val
        paths[key] = new_val

    with open('notebooks/paths.yml', 'w') as outfile:
        yaml.dump(data=paths, stream=outfile)

    dirs = [paths[elem] for elem in ['serialize', 'post', 'shapefiles']]

    for d in dirs:
        dir_path = Path(d)
        if not dir_path.is_dir():
            dir_path.mkdir(parents=False, exist_ok=True)
            print(f'Directory created: {dir_path}')
        else:
            print(f'Directory already exists: {dir_path}')

def set_credentials():
    username = input('Username for CDSE (or q to quit):')
    if username.lower == 'q':
        return None
    pswd = getpass.getpass('Password for CDSE:')

    with open('notebooks/paths.yml', 'r') as f:
        paths = yaml.safe_load(f)
    output_pref = paths['download']

    new_yaml = {'cop_dataspace':{'priority': None,
                                'search': None,
                                'download': {'extract': None, 'outputs_prefix': output_pref},
                                'auth': {'credentials': {'username': username, 'password': pswd}}}}
    
    eodag_path = Path.home() / '.config'/'eodag'/'eodag.yml'
    with open(eodag_path, 'w') as f:
        yaml.safe_dump(data=new_yaml, stream=f)

def main():
    make_subdirs()
    set_credentials()

if __name__ == '__main__':
    main()
