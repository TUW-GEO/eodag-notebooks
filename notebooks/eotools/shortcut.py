import os
import yaml
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from eodag import EODataAccessGateway
from dotenv import dotenv_values

def read_paths(path:str = "paths.yml"):
    '''
    This function gets the paths from paths.yml File and retrieves secrets from .env File.

    Params: 
        - path: Filepath to paths.yml
    
    Returns:
        - secrets
        - workspace
    '''
    # Get Paths
    with open(path, "r") as f:
        workspace = yaml.safe_load(f)

    # Get Secrets from .env File (defined in paths.yml)
    secrets = dotenv_values(workspace['credentials'])
    return secrets , workspace


def configure(dag:EODataAccessGateway, secrets:dict, paths:dict):
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

def deserialize(filepath:str, workspace:str, dag:EODataAccessGateway, log=True):
    # Deserialize the Search Results
    output_file = os.path.join(workspace['serialize'], filepath)
    deserialized_search_results = dag.deserialize_and_register(output_file)

    if log:
        print(f"Got {len(deserialized_search_results)} deserialized products.")

    return deserialized_search_results


