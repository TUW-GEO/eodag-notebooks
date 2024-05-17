import os
import yaml
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from eodag import EODataAccessGateway
from dotenv import dotenv_values

def prepare(path:str = "paths.yml", log:bool=True):
    '''
    This function gets the paths from paths.yml File and retrieves secrets from .env File.

    Params: 
        - path: Filepath to paths.yml
    
    Returns:
        - secrets
        - paths
    '''
    # Get Paths
    with open(path, "r") as f:
        paths = yaml.safe_load(f)

    # Get Secrets from .env File (defined in paths.yml)
    secrets = dotenv_values(paths['credentials'])

    # Check for Directories and create them if not exist
    directories = [paths['download'], paths['serialize'], paths['post'], paths['shapefiles']]
    for d in directories:
        if not os.path.isdir(d):
            ap = os.path.abspath(d)
            os.mkdir(ap)
            if log:
                print(f'Made Dir: {ap}')
        else:
            ap = os.path.abspath(d)
            if log:
                print(f'Dir exists: {ap}')

    return secrets, paths

def configure(secrets, paths):
    dag = EODataAccessGateway()
    dag.set_preferred_provider("cop_dataspace") # Copernicus Data Space Ecosystem

    dag.update_providers_config(f"""
        cop_dataspace:
            download:
                outputs_prefix: {os.path.abspath(paths['download'])}
            auth:
                credentials:
                    username: {secrets['USER_KEY']}
                    password: {secrets['USER_SECRET']}
    """)
    print(f'EODAG has been configured.')
    return dag

def plot_quicklooks(products):
    fig = plt.figure(figsize=(10,8))
    for i, product in enumerate(products[:12]):
        # This line takes care of downloading the quicklook
        quicklook_path = product.get_quicklook()
        
        date = product.properties['startTimeFromAscendingNode'][:16]
        provider = product.provider
        tile = product.properties['title'].split('_')[5].lstrip('T')
    
        # Plot the quicklook
        img = mpimg.imread(quicklook_path)
        ax = fig.add_subplot(3, 4, i+1)
        ax.set_title(f'Product {i}\n{date}\n{provider} - {tile}')
        ax.tick_params(top=False, bottom=False, left=False, right=False,
                       labelleft=False, labelbottom=False)
        plt.imshow(img)
    plt.tight_layout()