#Description
'''
This script is intended to simplify further processes in your code. 
In here you will find all the necessary functions to load data into xarray Datasets.
'''



#Variables:
__name__ = 'loading'
__version__ = '20-Jun-2024_v01'



#Modules:
import datetime as dt
import xarray as xr
import os
from eodag.utils.exceptions import AddressNotFound
from eodag import EOProduct, SearchResult, EODataAccessGateway
from pathlib import Path


def load_assets(root:str, res=60, only_spectral:bool=True, include_tci:bool=False) -> list[str]:
    '''
    Load all available assets/bands of a given product.

    Params:
    -------
        - root: str -> root directory of a downloaded product in SAFE format
        - res: int -> resolution of the bands to be loaded (10, 20, 60)
        - only_spectral: bool -> if True, only spectral bands are loaded
        - include_tci: bool -> if True, TCI (True Color Image) band is also loaded

    Returns:
    -------
        - assets: list[str] -> list of available assets/bands
    '''
    jp2_files = [file for dirs in os.walk(root, topdown=True)
                     for file in dirs[2] if file.endswith(f"_{res}m.jp2")]
    assets = [file.split('_')[2] for file in jp2_files if file.startswith('T')]

    if only_spectral and include_tci==False:
        assets = [a for a in assets if a[0]=='B']
    elif only_spectral and include_tci:
        assets = [a for a in assets if a[0] == 'B' or a[0] == 'T']
    else:
        pass
    
    return assets

def load_single_product(product: EOProduct, bands:list[str], **kwargs) -> xr.Dataset:
    '''
    Load multiple bands of a single product into an xarray Dataset.

    Params:
    -------
        - product: EOProduct -> product to be loaded
        - bands: list[str] -> list of bands to be loaded (provided by ``load_assets`` function)
        - **kwargs: dict -> additional arguments to be passed to the ``get_data`` method of the EOProduct (``common_params``)

    Returns:
    -------
        - ds: xarray.Dataset -> xarray Dataset containing the loaded bands
    '''
    loaded_data = {}
    for band in bands:
        # Load Band into an xarray Dataarray
        data = product.get_data(band=band, **kwargs)

        # Get rid of Dimensions of size 1 [e.g.: shapes from (1,300,500) to (300,500)]
        data = data.squeeze()

        # Get time information from the product properties
        time_str = product.properties['startTimeFromAscendingNode']
        date = dt.datetime.strptime(time_str,'%Y-%m-%dT%H:%M:%S.%f%z')

        # Add a timestamp to the xarray dataarray (taken from product properties)
        data = data.expand_dims(dim={'time':[date.date()]})

        # Name the Dataarray (band name is used) -> Dataset uses the Dataarray name to name its variables
        data.name = band

        # Add Dataarray of a single band to the loaded_data dictionary
        loaded_data[band] = data
    # Create a xarray Dataset from a dictionary of Dataarrays
    ds = xr.Dataset(loaded_data)
    return ds

def load_multiple_timestamps(products:SearchResult, bands:list, *args, **kwargs) -> xr.Dataset:
    '''
    Load multiple bands of multiple products into an xarray Dataset. 
    Do not use different geographical areas, as merging needs to be done beforehand.

    Params:
    -------
        - products: list[EOProduct] -> list of products to be loaded
        - bands: list[str] -> list of bands to be loaded (provided by ``load_assets`` function)
        - **kwargs: dict -> additional arguments to be passed to the ``get_data`` method of the EOProduct (``common_params``)

    Returns:
    -------
        - ds: xarray.Dataset -> xarray Dataset containing the loaded bands from all products
    '''
    # Empty List where datasets are stored
    single_ds = []
    for product in products:
        # Load each dataarray and add to single_ds List
        single_product = load_single_product(product=product, bands=bands, *args, **kwargs)
        single_ds.append(single_product)
    # Merge datasets from List
    ds = xr.merge(single_ds)
    return ds


##############################################
# Regex functions
##############################################

def band_2_regex(band:str) -> tuple[str]:
    '''
    Transform a band name into a regex pattern to be used in the ``get_data`` method of the EOProduct.
    Needs the newest version of eodag-cube (>= 0.4.1) to work properly 
    or install from source (``pip install git+https://github.com/CS-SI/eodag-cube.git``).

    Params:
    -------
        - band: str -> band name to be transformed into a regex pattern

    Returns:
    -------
        - (r10, r20, r60): list[str] -> list of regex patterns for 10m, 20m, and 60m resolution bands
    '''
    # regex = rf'^(?!.*MSK).*{band}_[0-9]*m.jp2$'
    r10 = rf'^(?!.*MSK).*{band}_10m.jp2$'
    r20 = rf'^(?!.*MSK).*{band}_20m.jp2$'
    r60 = rf'^(?!.*MSK).*{band}_60m.jp2$'
    return r10, r20, r60

def load_single_product_regex(product, bands:list[str], **kwargs) -> xr.Dataset:
    '''
    Load multiple bands of a single product into an xarray Dataset using regex patterns.

    Params:
    -------
        - product: EOProduct -> product to be loaded
        - bands: list[str] -> list of bands to be loaded (provided by ``load_assets`` function)
        - **kwargs: dict -> additional arguments to be passed to the ``get_data`` method of the EOProduct (``common_params``)

    Returns:
    -------
        - ds: xarray.Dataset -> xarray Dataset containing the loaded bands
    '''
    loaded_data = {}
    for band in bands:
        regex = band_2_regex(band=band)
        # Load Band into an xarray Dataarray
        for r in regex:
            try:
                data = product.get_data(band=r, **kwargs)
                break
            except:
                AddressNotFound
        
        # Get rid of Dimensions of size 1 [e.g.: shapes from (1,300,500) to (300,500)]
        data = data.squeeze()

        # Get time information from the product properties
        time_str = product.properties['startTimeFromAscendingNode']
        date = dt.datetime.strptime(time_str,'%Y-%m-%dT%H:%M:%S.%f%z')

        # Add a timestamp to the xarray dataarray (taken from product properties)
        data = data.expand_dims(dim={'time':[date.date()]})

        # Name the Dataarray (band name is used) -> Dataset uses the Dataarray name to name its variables
        data.name = band

        # Add Dataarray of a single band to the loaded_data dictionary
        loaded_data[band] = data
    # Create a xarray Dataset from a dictionary of Dataarrays
    ds = xr.Dataset(loaded_data)
    return ds

def load_multiple_timestamps_regex(products, bands:list, **kwargs) -> xr.Dataset:
    '''
    Load multiple bands of multiple products into an xarray Dataset using regex patterns.

    Params:
    -------
        - products: list[EOProduct] -> list of products to be loaded
        - bands: list[str] -> list of bands to be loaded (provided by ``load_assets`` function)
        - **kwargs: dict -> additional arguments to be passed to the ``get_data`` method of the EOProduct (``common_params``)

    Returns:
    -------
        - ds: xarray.Dataset -> xarray Dataset containing the loaded bands from all products
    '''
    # Empty List where datasets are stored
    single_ds = []
    for product in products:
        # Load each dataarray and add to single_ds List
        single_product = load_single_product_regex(product=product, bands=bands, **kwargs)
        single_ds.append(single_product)
    # Merge datasets from List
    ds = xr.merge(single_ds)
    return ds

def get_data_regex(product, band:str, **kwargs):
    '''
    Load a single band of a single product using regex patterns.

    Params:
    -------
        - product: EOProduct -> product to be loaded
        - band: str -> band to be loaded
        - **kwargs: dict -> additional arguments to be passed to the ``get_data`` method of the EOProduct (``common_params``)

    Returns:
    -------
        - data: xarray.DataArray -> xarray DataArray containing the loaded band
    '''
    regex = band_2_regex(band)
    for r in regex:
        try:
            data = product.get_data(band=r, **kwargs)
            break
        except:
            AddressNotFound
    return data

##############################################
# Reverse Search functions
##############################################

def extract_infos_from_filename(file:Path|str) -> dict:
    '''
    Takes a Path object and extracts the following information from the filename:
    - product_type
    - start_date
    - end_date
    - tile

    Returns a dictionary with the extracted information.

    Params:
    -------
        - file (Path|str): Path object or string with the following naming convention:
        ``<platform>_<instrument><product_level>_<sensing_datetime>_<processing_pipeline>_<orbit>_<tile>_<processing_date>``

    Returns:
    -------
        - data (dict): Dictionary containing the extracted information
    '''
    data = {}
    if type(file) != str:
        id = file.name
    elif type(file) == str:
        id = file
    else:
        raise TypeError('Please provide a Path object or a string.')
    
    platform= id.split('_')[0].rstrip('AB')
    instrument= id.split('_')[1][:3]
    product_level = id.split('_')[1][3:]
    data['product_type'] = '_'.join([platform, instrument, product_level])

    sensing_date = id.split('_')[2].split('T')[0]
    date = dt.datetime.strptime(sensing_date, '%Y%m%d')
    data['start_date'] = date.strftime('%Y-%m-%d')
    data['end_date'] = (date + dt.timedelta(days=1)).strftime('%Y-%m-%d')

    data['tile'] = id.split('_')[5].lstrip('T')
    return data

def search_for_file(file:Path|str, provider:str='cop_dataspace') -> EOProduct|None:
    '''
    Searches for a file in the EODAG database based on the filename.

    Params:
    -------
        - file (Path|str): Path object or string following the naming convention
        - provider (str): Provider to search for the file
        
    Returns:
    -------
        - found_product (EOProduct): EOProduct object found in the database
    '''
    dag = EODataAccessGateway()

    if type(file) != str:
        id = file.name
    elif type(file) == str:
        id = file
    else:
        raise TypeError('Please provide a Path object or a string.')
    
    data = extract_infos_from_filename(id)
    search_results, _ = dag.search(
        productType=data['product_type'],
        provider=provider,
        tileIdentifier=data['tile'],
        start=data['start_date'],
        end=data['end_date'],
        cloudCover=100 
    )

    
    
    for found_product in search_results:
        try:
            if found_product.properties['id'] == id:
                return found_product
        except:
            print('No matching file found.')
            return None
        
def directory_to_search_results(directory:list[Path]|list[str], provider:str='cop_dataspace') -> SearchResult:
    '''
    Searches for all files in a directory in the EODAG database based on the filename.
    Returns a SearchResult object with all found files.

    Params:
    -------
        - directory (list[Path]|list[str]): List of Path objects or strings following the naming convention
        - provider (str): Provider to search for the files

    Returns:
    -------
        - results (SearchResult): SearchResult object with all found files
    '''
    results = SearchResult([])
    for file in directory:
        result = search_for_file(file=file, provider=provider)
        if result:
            results.append(result)
    return results