# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 09:47:10 2024

This Script showcases the useage of Environment Variables to pass Credentials 
to EODAG.
"""
#Imports
import os
from eodag import EODataAccessGateway

#%%
#Set Credentials for Copernicus Dataspace Ecosystem (CDSE) as Environment Variable.
#Once you have set your credentials you may delete them from this code and mark out 
#the next two lines. Your Variables, if not changed, should still be saved in the background.
os.environ["EODAG__CDSE__AUTH__CREDENTIALS__USERNAME"] = "PLEASE_CHANGE_USERNAME"
os.environ["EODAG__CDSE__AUTH__CREDENTIALS__PASSWORD"] = "PLEASE_CHANGE_PASSWORD"

#Execut the following two lines to delete Environment Variables again, if not needed anymore.
#os.environ.pop("EODAG__CDSE__AUTH__CREDENTIALS__USERNAME")
#os.environ.pop("EODAG__CDSE__AUTH__CREDENTIALS__PASSWORD")

user_key = os.getenv("EODAG__CDSE__AUTH__CREDENTIALS__USERNAME")
user_secret = os.getenv("EODAG__CDSE__AUTH__CREDENTIALS__PASSWORD")

#%%
#Create EODAG Object and set preferred Provider
dag = EODataAccessGateway()
dag.set_preferred_provider("cop_dataspace") # Copernicus Data Space Ecosystem

#Configure EODAG (Getting Started) (Passing Username and Password to EODAG)
dag.providers_config['cop_dataspace'].auth.credentials['username'] = user_key
dag.providers_config['cop_dataspace'].auth.credentials['password'] = user_secret