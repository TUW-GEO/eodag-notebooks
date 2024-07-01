<img src ="https://eodag.readthedocs.io/en/latest/_static/eodag_bycs.png" width=200>

<img src="https://dataspace.copernicus.eu/sites/default/files/styles/opengraph/public/media/images/2023-03/og_share.png?itok%253DzjtW85Fb" width="200">

# eodag-workflows

This repository stores an example gallery repo for loading and processing Sentinel Data from Copernicus Dataspace Ecosystem useing EODAG. 
The repo contains the following elements in the ``notebooks`` directory:

- `01_eodag_search.ipynb` A notebook just for the Search of EO Data 
- `02_eodag_des_post.ipynb` A notebook for downloading the Data from serialized search results 
- `03_eodag_img_pro.ipynb` A notebook for image processing 
- `04_eodag_search_post.ipynb` A notebook for searching and downloading without serialization (the workflow as intended by EODAG)
- `05_eodag_merging.ipynb` A notebook for combining EO data temporarily and geospatialy 
- `06_eodag_classify.ipynb` A notebook for different classification processes 
- `07_eodag_roi.ipynb` A Notebook which shows how to create Geojsons of Regions of Interest.

# Before getting started
In order to acquire and process Sentinel Data you will need to have an account at [Copernicus Dataspace Ecosystem (CDSE)](https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/auth?client_id=cdse-public&response_type=code&scope=openid&redirect_uri=https%3A//dataspace.copernicus.eu/account/confirmed/1). Use the provided Link or visit: *https://dataspace.copernicus.eu/*

# Getting started on Jupyterlab
Copy the provided `Makefile` into your `HOME` directory. Open a Terminal (where you placed the `Makefile`) and type the following command.
```bash
make all
```
This command will:

- pull the **notebooks** from the Git repository
- execute the ``setup.py`` file from the repo (adds some folders to store data and creates a config file where your Credentials for CDSE will be stored)
- create a conda **environment** from ``environment.yml`` file
- and creates a **kernel**

So have your credentials for CDSE ready when running this command, or run the `setup.py` file later on to set your credentials. The ``makefile`` has a `make setup` command, which will do that for you.

After the setup has finished you will find the following files in your directory.

```sh
eodag-notebooks
├── Makefile
├── README.md
├── environment.yml
├── setup.py
├── notebooks
│   ├── 01_eodag_search.ipynb       # Searching for Data
│   ├── 02_eodag_des_post.ipynb     # Download Data from serialized Search
│   ├── 03_eodag_img_pro.ipynb      # Image Processing (Contrast, Stacking,...)
│   ├── 04_eodag_search_post.ipynb  # Search and Postprocessing
│   ├── 05_eodag_merging.ipynb      # Merging of overlapping Geographical extents
│   ├── 06_eodag_classify.ipynb     # Classification
│   ├── 07_eodag_roi.ipynb          # Polygons of regions of Interest
│   ├── paths.yml
│   └── paths_temp.yml
├── postprocess     # Directory where you can store your Results
├── serialize       # Directory where you can store serialized searches
└── shapefiles      # Directory where you can store shapefiles (geojson)
```
Here you find the Notebooks 01 - 07 each of them explains something different. 
It is advised, that you create a new notebook and use all the code-snippets which you would like to use yourself from the provided notebooks.

## Permissions 
As a student you have *read and write* permissions in your `HOME` directory. Furthermore you have *reading* rights in the `shared` directory. Here we have a directory
`shared/datasets/rs/datapool/download` where we can store the data you would like to use for your work. As you do not have rights to download data there you have two options.

1. Provide a `search_results.geojson` file (see Notebook 1) and we will download the data for you onto the Jupyterlab.
2. Download the data to your home directory by changeing the download path in the `paths.yml` file.