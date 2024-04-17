![EODAG]( https://eodag.readthedocs.io/en/latest/_static/eodag_bycs.png)

![CDSE](![https://dataspace.copernicus.eu/themes/custom/copernicus/logo.svg](https://dataspace.copernicus.eu/sites/default/files/styles/opengraph/public/media/images/2023-03/og_share.png?itok%253DzjtW85Fb))

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
- `00_git-tutorial.ipynb` A notebook for explaining git 
- Additionaly different scripts explaining the passing of credentials to EODAG methods

To properly run the notebooks, you will need to create a file called `.env` which includes your credentials to the 
Copernicus Dataspace Ecosystem. The files contents should look similar to the following:
```
USER_KEY = "CHANGE_USERNAME"
USER_SECRET = "CHANGE_PASSWORD"
```