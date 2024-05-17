import rioxarray
import geopandas as gpd
from shapely.geometry import mapping

def clip_dataset_2_shapefile(ds, shapefile):
    clip_shape = gpd.read_file(shapefile)
    ds = ds.rio.clip(clip_shape.geometry.apply(mapping), clip_shape.crs, drop=False, invert=False)
    return ds