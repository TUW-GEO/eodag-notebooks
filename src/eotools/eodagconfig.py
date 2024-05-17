import os
import yaml

from eodag import EODataAccessGateway
from dotenv import dotenv_values

def get_secrets():
    # Define all paths in paths.yml file. 
    with open("paths.yml", 'r') as f:
        paths = yaml.safe_load(f)
    
    secrets = dotenv_values(paths['credentials'])

    workspaces = [paths['download'], paths['serialize'], paths['post'], paths['shapefiles']]

    for ws in workspaces:    
        if not os.path.isdir(ws):
            ws = os.path.abspath(ws)
            os.mkdir(ws)
            print(f'Created Folder: {ws}')
        else:
            ws = os.path.abspath(ws)
            print(f'Folder already exists: {ws}')
            
    return 

def configure_eodag(file:str, cred_path:str):
    '''
    Takes a serialized Search Result from EODAG and the Credentials to Configure the DAG Object.
    Params:
        - file: Filepath of search result.
    '''
    # Get Secrets 
    secrets = dotenv_values(cred_path)

    #Create Folders for saving Data, serializing and post processing.
    root = '../eodag-data/'

    workspace_download = os.path.join(root,'eodag_workspace_download')
    workspace_serialize = os.path.join(root,'eodag_workspace_serialize_deserialize')

    #Create EODAG Object and set preferred Provider
    dag = EODataAccessGateway()
    dag.set_preferred_provider("cop_dataspace") # Copernicus Data Space Ecosystem

    dag.update_providers_config(f"""
        cop_dataspace:
            download:
                outputs_prefix: {os.path.abspath(workspace_download)}
            auth:
                credentials:
                    username: {secrets['USER_KEY']}
                    password: {secrets['USER_SECRET']}
    """)

    # Deserialize the Search Results
    output_file = os.path.join(workspace_serialize, file)
    deserialized_search_results = dag.deserialize_and_register(output_file)

    print(f"Got {len(deserialized_search_results)} deserialized products.")
    return deserialized_search_results

if __name__ == "__main___":
    pass