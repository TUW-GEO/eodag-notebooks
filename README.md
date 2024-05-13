<img src ="https://eodag.readthedocs.io/en/latest/_static/eodag_bycs.png" width=200>

<img src="https://dataspace.copernicus.eu/sites/default/files/styles/opengraph/public/media/images/2023-03/og_share.png?itok%253DzjtW85Fb" width="200">

# eodag-workflows

This repository stores an example gallery repo for loading and processing Sentinel Data from Copernicus Dataspace Ecosystem useing EODAG. 
The Notebooks are numbered in the order that we want them to appear on the gallery website.
The repo contains the following elements:

- `01_eodag_search.ipynb` A notebook just for the Search of EO Data 
- `02_eodag_des_post.ipynb` A notebook for downloading the Data from serialized search results 
- `03_eodag_img_pro.ipynb` A notebook for image processing 
- `04_eodag_search_post.ipynb` A notebook for searching and downloading without serialization (the workflow as intended by EODAG)
- `05_eodag_merging.ipynb` A notebook for combining EO data temporarily and geospatialy 
- `06_eodag_classify.ipynb` A notebook for different classification processes 
- `00_xarray-tutorial.ipynb` A notebook for explaining xarrays 
- `00_git-tutorial.md` A notebook for explaining git 
- Additionaly different scripts explaining the passing of credentials to EODAG methods

To properly run the notebooks, you will need to create a file called `.env` which includes your credentials to the 
Copernicus Dataspace Ecosystem. The files contents should look similar to the following:
```
USER_KEY = "CHANGE_USERNAME"
USER_SECRET = "CHANGE_PASSWORD"
```

# Access

In order to use the notebooks the best way would be to `clone` the repo. It is also possible to download the different notebooks individually. 
Use the following command to `clone` the repo.

```
git clone <URL_to_Github_repo>
```
## Conda
If you want to use the Notebooks it would be best to create a new Environment either with:
```
conda env create -n eoenv --file eoenv.yml
```
or
```
conda create -n eoenv --file requirements.txt
```
## Venv
Or if `conda` is not installed create an environment with venv
```
python -m venv .eoenv
```
activate the environment on windows with 
```
activate
```
or on Linux 
```
source .venv/bin/activate
```
and then install all Packages with pip
```
pip install -r requirements.txt
```