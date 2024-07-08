#Description
'''
This script is intended to simplify further processes in your code. 
In here you will find all the necessary functions to manipulate the quality 
and contrasts of your produced tif images.
'''



#Variables:
__name__ = 'contrast'
__version__ = '20-Jun-2024_v01'



#Modules:
import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray
import xarray as xr



#Functions
def auto_clip(I:ndarray, percentile:float=0.02, pooled:bool=True) -> ndarray:
    """ 
    Calculates the quantiles of I using the percentile parameter and clips the values using the clip function defined below.
    Modifies I
    
    Params:
    ----------
        - I : np.array(rows, cols, bands)
            Image array.
        - percentile : float, optional
            Percentile defining the clipping boundaries of I in terms of its distribution (defaults to 0.02). 
        - pooled: if True, computes the pooled percentile over all band
                (default, use this to keep the relative intensities of the bands for natural looking images)    
                if False, computes the percentiles for each band individually
                (use this - in conjunction with stretch - to bring the different bands into a comparable range, e.g. for false colour images)
        
    
    Returns:
    -------
        - np.array : Auto-clipped image data.
    
    """
    if pooled:
        v_min = np.nanquantile(I, percentile)
        v_max = np.nanquantile(I, 1 - percentile)
 
    else:
        tmp = I.reshape(-1, I.shape[-1]) #collapes image x,y 2d-array into a 1d-array
        v_min = np.nanquantile(tmp, percentile, axis=0)
        v_max = np.nanquantile(tmp, 1 - percentile, axis=0)
        
    return clip(I, v_min, v_max)        

def clip(I:ndarray, v_min:float, v_max:float) -> ndarray:
    """ 
    Performs clipping (dt. "Histogrammbegrenzung")
    Sets all values in I that are outside of [v_min, v_max] to the corresponding boundary.
    Modifies I
    
    Params:
    ----------
        - I : np.array
            Image array.
        - v_min : scalar or array
            Lower clipping boundary for each band
        - v_max : scalar or array
            lower clipping boundary for each band
    
    Returns:
    -------
        - np.array : Clipped image data.
        
    """
        
    tmp = I.reshape(-1, I.shape[-1]) #collapes image x,y 2d-array into a 1d-array         
    if np.isscalar(v_min):
        tmp[tmp < v_min] = v_min
        tmp[tmp > v_max] = v_max
    else:
        idx = np.where(tmp < v_min)
        tmp[idx]=v_min[idx[1]]
        idx = np.where(tmp > v_max)
        tmp[idx]=v_max[idx[1]]        
    
    return I

def stretch(I:ndarray, p_min:float, p_max:float, pooled:bool=True) -> ndarray:
    """
    Performs histogram stretching or normalisation (dt. "Spreizung")
    Computes and applies an affine transformation of values in I to the range [p_min, p_max]. 
    For floating point images to be displayed with pylab.imshow(), p_min=0, p_max=1
    should be chosen.
    Modifies I
    
    Params:
    ----------
        - I : np.array
            Image array.
        - p_min : number
            Lower boundary of the output range.
        - p_max : number
            Upper  boundary of the output range.
        - pooled: if True, the transformation is computed for and applied to all bands simultaneously  
                if False, -"- to the individual bands separately

    Returns:
    -------
        - np.array : Normalised image data within the range [p_min, p_max].
    
    """
    tmp = I.reshape(-1, I.shape[-1]) #collapes image x,y 2d-array into a 1d-array   

    if pooled:    
        q_min = np.nanmin(I)
        q_max = np.nanmax(I)

    else:
             
        q_min = np.nanmin(tmp, axis = 0)
        q_max = np.nanmax(tmp, axis = 0)        

    tmp[:] =  (p_max - p_min) * (tmp - q_min) / (q_max - q_min) + p_min
    return I

def histogram(data:xr.DataArray|ndarray, nbins:int=256, alpha:float=0.5, figsize:tuple=(5,5),
              title:str='Histogram', xlim:float|int=None, ylim:float|int=None, **kwargs) -> None:
    '''
    Plot the histogram of the dataset.

    Params:
    -------
        - dataset: xr.Dataset -> dataset with only one data variable
        - nbins: int -> number of bins to be used in the histogram (default=256)
        - alpha: float -> transparency of the histogram bars
        - figsize: tuple -> size of the figure
        - title: str -> title of the plot
        - xlim: float|int -> x-axis limits
        - ylim: float|int -> y-axis limits
    
    Returns:
    -------
        - None
        - Shows the histogram plot
    '''
    #Flatten
    if type(data) == xr.DataArray:
        arr = data.values
    elif type(data) == ndarray:
        arr = data
    else:
        raise TypeError('The data should be either a xr.Dataset or a np.ndarray')

    # You can set the number of bins and alpha individually
    mbins = np.linspace(np.nanmin(arr), np.nanmax(arr), nbins)

    colors=['red', 'green', 'blue', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

    # Plot 
    if 'ax' in kwargs:
        ax = kwargs['ax']
    else:
        fig, ax = plt.subplots(figsize=figsize)

    if len(arr.shape) == 2:
        flat = arr.flatten()
        ax.hist(flat, color=colors[0], bins=mbins, alpha=alpha, zorder=0)
    elif type(data) == ndarray:
        for color in range(arr.shape[-1]):
            flat = arr[:, :, color].flatten()
            ax.hist(flat, color=colors[color], bins=mbins, alpha=alpha, zorder=color)
    else:
        for color in range(arr.shape[0]):
            flat = arr[color, :, :].flatten()
            ax.hist(flat, color=colors[color], bins=mbins, alpha=alpha, zorder=color)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.set_title(title)
    ax.set_xlabel('I (Intensity)')
    ax.set_ylabel('n (Frequency)')
    
    plt.show()


def auto_clip_dataarray(dataarray: xr.DataArray, percentile: float = 0.02, pooled: bool = True) -> xr.DataArray:
    '''
    This function clips the values of a DataArray using the auto_clip function.

    Params:
    -------
        - dataarray: xr.DataArray -> DataArray to be clipped
        - percentile: float -> percentile defining the clipping boundaries of I in terms of its distribution (defaults to 0.02)
        - pooled: bool -> if True, computes the pooled percentile over all bands
                          if False, computes the percentiles for each band individually

    Returns:
    --------
        - xr.DataArray: Clipped DataArray.
    '''
    # Extract the numpy array from the DataArray
    I = dataarray.values
    
    # Apply the auto_clip function
    clipped_array = auto_clip(I, percentile, pooled)
    
    # Create a new DataArray with the clipped values, preserving the original coordinates and attributes
    clipped_dataarray = xr.DataArray(clipped_array, dims=dataarray.dims, coords=dataarray.coords, attrs=dataarray.attrs)
    
    return clipped_dataarray

def auto_clip_dataset(ds, *args, **kwargs):
    '''
    This function clips the values of a Dataset using the auto_clip_dataarray function.

    Params:
    -------
        - ds: xr.Dataset -> Dataset to be clipped
        - *args: -> arguments to be passed to the auto_clip_dataarray function
        - **kwargs: -> keyword arguments to be passed to the auto_clip_dataarray function

    Returns:   
    --------
        - xr.Dataset: Clipped Dataset.
    '''
    ds = ds.copy()
    for var in ds.data_vars:
        clipped = auto_clip_dataarray(ds[var].copy(), *args, **kwargs)
        ds[var] = clipped
    return ds

def stretch_dataarray(dataarray: xr.DataArray, p_min: float, p_max: float, pooled: bool = True) -> xr.DataArray:
    '''
    This function stretches the values of a DataArray using the stretch function.

    Params:
    -------
        - dataarray: xr.DataArray -> DataArray to be stretched
        - p_min: float -> lower boundary of the output range
        - p_max: float -> upper boundary of the output range
        - pooled: bool -> if True, the transformation is computed for and applied to all bands simultaneously
                          if False, the transformation is computed for and applied to the individual bands separately

    Returns:
    --------
        - xr.DataArray: Stretched DataArray.
    '''
    # Extract the numpy array from the DataArray
    I = dataarray.values
    
    # Apply the stretch function
    stretched_array = stretch(I, p_min, p_max, pooled)
    
    # Create a new DataArray with the stretched values, preserving the original coordinates and attributes
    stretched_dataarray = xr.DataArray(stretched_array, dims=dataarray.dims, coords=dataarray.coords, attrs=dataarray.attrs)
    
    return stretched_dataarray
