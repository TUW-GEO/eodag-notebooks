#Description
'''
This script is intended to simplify further processes in your code. 
In here you will find all the necessary functions to shorten the notebooks and to make it more readable.
'''



#Variables:
__name__ = 'shortcut'
__version__ = '20-Jun-2024_v01'



#Modules:
import os
import yaml
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from eodag import EODataAccessGateway, SearchResult, EOProduct
from pathlib import Path


def read_paths(filepath:str = "paths.yml") -> dict:
    '''
    This function gets the paths from paths.yml File and retrieves secrets from .env File.

    Params: 
    -------
        - path: Filepath to ``paths.yml``
    
    Returns:
    --------
        - workspace: dict -> Dictionary containing the paths
    '''
    src = Path(filepath).resolve()
    with open(src, "r") as f:
        workspace = yaml.safe_load(f)

    return workspace


def configure(dag:EODataAccessGateway, secrets:dict, paths:dict) -> EODataAccessGateway:
    '''
    This function configures the EODAG with the necessary credentials and paths.

    Params:
    -------
        - dag: EODataAccessGateway -> EODAG Object
        - secrets: dict -> Dictionary containing the secrets
        - paths: dict -> Dictionary containing the paths

    Returns:
    --------
        - dag: EODataAccessGateway -> Configured EODAG Object
    '''
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

def plot_quicklooks(products:SearchResult|list[EOProduct]) -> None:
    '''
    Plot the quicklooks of the products.

    Params:
    -------
        - products: SearchResult -> SearchResult object containing the products

    Returns:
    --------
        - None
        - Shows the quicklooks of the products
    '''
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

def deserialize(filename:str, workspace:str, dag:EODataAccessGateway, log=True) -> SearchResult|list[EOProduct]:
    '''
    Deserialize and register the Search Results.

    Params:
    -------
        - filename: str -> Filename of the serialized file
        - workspace: str -> Filepath to the workspace (directory where the serialized file is stored)
        - dag: EODataAccessGateway -> EODAG Object
        - log: bool -> if True, print the number of deserialized products

    Returns:
    --------
        - Deserialized SearchResult object
    '''
    # Deserialize the Search Results
    output_file = os.path.join(workspace['serialize'], filename)
    deserialized_search_results = dag.deserialize_and_register(output_file)

    if log:
        print(f"Got {len(deserialized_search_results)} deserialized products.")

    return deserialized_search_results


