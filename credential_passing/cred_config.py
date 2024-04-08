# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 09:47:10 2024

This Script showcases the useage of Environment Variables to pass Credentials 
to EODAG.
"""
#Imports
from eodag import EODataAccessGateway


#%%
#Set Credentials for Copernicus Dataspace Ecosystem (CDSE) in YAML Config File from EODAG.
dag = EODataAccessGateway()
dag.update_providers_config("""
    cop_dataspace:
        download:
            outputs_prefix:
        auth:
            credentials:
                username: PLEASE_CHANGE_USERNAME
                password: PLEASE_CHANGE_PASSWORD
""")

dag.set_preferred_provider("cop_dataspace") # Copernicus Data Space Ecosystem