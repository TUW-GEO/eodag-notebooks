<img src ="https://eodag.readthedocs.io/en/latest/_static/eodag_bycs.png" width=200>

<img src="https://dataspace.copernicus.eu/sites/default/files/styles/opengraph/public/media/images/2023-03/og_share.png?itok%253DzjtW85Fb" width="200">

# eodag-workflows

This repository stores an example gallery repo for loading and processing Sentinel Data from Copernicus Dataspace Ecosystem useing EODAG. 
The Notebooks are numbered in the order that we want them to appear on the gallery website.
The repo contains the following elements in the ``notebooks`` directory:

- `01_eodag_search.ipynb` A notebook just for the Search of EO Data 
- `02_eodag_des_post.ipynb` A notebook for downloading the Data from serialized search results 
- `03_eodag_img_pro.ipynb` A notebook for image processing 
- `04_eodag_search_post.ipynb` A notebook for searching and downloading without serialization (the workflow as intended by EODAG)
- `05_eodag_merging.ipynb` A notebook for combining EO data temporarily and geospatialy 
- `06_eodag_classify.ipynb` A notebook for different classification processes 
- `07_eodag_roi.ipynb` A Notebook which shows how to create Geojsons of Regions of Interest.

- Additionaly different scripts explaining the passing of credentials to EODAG methods

To properly run the notebooks, you will need to create a file called `.env` which includes your credentials to the 
Copernicus Dataspace Ecosystem. The files contents should look similar to the following:
```c
USER_KEY = "CHANGE_USERNAME"
USER_SECRET = "CHANGE_PASSWORD"
```

These credentials need to be set on [the website of Copernuicus](https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/auth?client_id=cdse-public&response_type=code&scope=openid&redirect_uri=https%3A//dataspace.copernicus.eu/account/confirmed/1). __DO NOT USE SENSITIVE PASSWORDS__, as others might see your credentials on the jupyterhub.

# Setup
To use this Repository on Jupyterhub (or locally) you can use the ``Makefile`` to pull this repository and create the environment aswell as the kernel.
The make file uses `mamba` to install the `kernel` and the `environment`. If you don't have mamba installed 
you will need to manually change the Makefile commands (swap `mamba` with `conda`)

When you have done the setup correctly (executed `make all`) your directory should look something like this:

```bash
eodag-notebooks
├── Makefile
├── README.md
├── environment.yml
├── setup.py
├── notebooks
│   ├── 01_eodag_search.ipynb
│   ├── 02_eodag_des_post.ipynb
│   ├── 03_eodag_img_pro.ipynb
│   ├── 04_eodag_search_post.ipynb
│   ├── 05_eodag_merging.ipynb
│   ├── 06_eodag_classify.ipynb
│   ├── 07_eodag_roi.ipynb
│   ├── paths.yml
│   └── paths_temp.yml
├── postprocess     # Directory where you can store your Results
├── serialize       # Directory where you can store serialized searches
└── shapefiles      # Directory where you can store shapefiles (geojson)
```
You should not mind most of the files. Use the `notebooks` to write your own code for your work and try to use the provided folder for saving data. 
You can still absolutely modify the setup to your likeing.
 
## Working on the Jupyterhub
When you work on the Jupyterhub copy the `Makefile` into your Directory and execute the following command in a terminal:
```bash
make all
```

## Working locally
If you work locally you will have to clone the Repository with:

```bash
git clone https://github.com/npikall/eodag-notebooks.git
```

In order to create a new environment with the right dependencies and to create an Python ``kernel`` you can use the make file as follows.
```bash
make kernel
```

In the case you just need the ``environment`` installed use this:
```bash
make environment
```

Also use the following __(optional)__ to execute the ``setup.py`` file, which will create a custom ``paths.yml`` file from the template
and create the subdirectories specified in the paths file.
```bash
make setup
```

And to remove the `kernel` aswell as the `environment` use
```bash
make teardown
```
### Alternative Conda
If you want to work locally you can also use either `conda` or `mamba` to create the right environments.
If you want to use the Notebooks it would be best to create a new Environment with:
```bash
conda env create -n ENVNAME --file environment.yml
```
Change `ENVNAME` to whatever you want to call the environment.