# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 09:47:10 2024

This Script showcases the useage of the dotenv Module to pass Credentials 
to EODAG.
"""
#Imports
from eodag import EODataAccessGateway
from dotenv import dotenv_values

#%%
#Retrieve Credentials for Copernicus Dataspace Ecosystem (CDSE) from .env file 
secrets = dotenv_values('.env')
user_key = secrets['USER_KEY']
user_secret = secrets['USER_SECRET']

#%%
#Create EODAG Object and set preferred Provider
dag = EODataAccessGateway()
dag.set_preferred_provider("cop_dataspace") # Copernicus Data Space Ecosystem

#Configure EODAG (Getting Started) (Passing Username and Password to EODAG)
dag.providers_config['cop_dataspace'].auth.credentials['username'] = user_key
dag.providers_config['cop_dataspace'].auth.credentials['password'] = user_secret