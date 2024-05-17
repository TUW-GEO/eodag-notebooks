#Description
'''
This script is intended to simplify further processes in your code. 
In here you will find all the necessary functions to manipulate the quality 
and contrasts of your produced tif images.
'''



#Variables:
__name__ = 'contrast'
__version__ = '04-Aug-2023_v01'



#Modules:
import numpy as np



#Functions
def auto_clip(I, percentile=0.02, pooled=True):
    """ 
    Calculates the quantiles of I using the percentile parameter and clips the values using the clip function defined below.
    
    Modifies I
    
    Parameters
    ----------
    I : np.array(rows, cols, bands)
        Image array.
    percentile : float, optional
        Percentile defining the clipping boundaries of I in terms of its distribution (defaults to 0.02). 
    pooled: if True, computes the pooled percentile over all band
            (default, use this to keep the relative intensities of the bands for natural looking images)    
            if False, computes the percentiles for each band individually
            (use this - in conjunction with stretch - to bring the different bands into a comparable range, e.g. for false colour images)
        
    
    Returns
    -------
    np.array : 
        Auto-clipped image data.
    
    """
    if pooled:
        v_min = np.nanquantile(I, percentile)
        v_max = np.nanquantile(I, 1 - percentile)
 
    else:
        tmp = I.reshape(-1, I.shape[-1]) #collapes image x,y 2d-array into a 1d-array
        v_min = np.nanquantile(tmp, percentile, axis=0)
        v_max = np.nanquantile(tmp, 1 - percentile, axis=0)
        
    return clip(I, v_min, v_max)        

def clip(I, v_min, v_max):
    """ 
    Performs clipping (dt. "Histogrammbegrenzung")
    Sets all values in I that are outside of [v_min, v_max] to the corresponding boundary.

    
    Modifies I
    
    Parameters
    ----------
    I : np.array
        Image array.
    v_min : scalar or array
        Lower clipping boundary for each band
    v_max : scalar or array
        lower clipping boundary for each band
    
    Returns
    -------
    np.array : 
        Clipped image data.
        
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

def stretch(I, p_min, p_max, pooled=True):
    """
    Performs histogram stretching or normalisation (dt. "Spreizung")
    Computes and applies an affine transformation of values in I to the range [p_min, p_max]. 
    For floating point images to be displayed with pylab.imshow(), p_min=0, p_max=1
    should be chosen.
    
    Modifies I
    
    Parameters
    ----------
    I : np.array
        Image array.
    p_min : number
        Lower boundary of the output range.
    p_max : number
        Upper  boundary of the output range.
    pooled: if True, the transformation is computed for and applied to all bands simultaneously  
            if False, -"- to the individual bands separately
    Returns
    -------
    np.array : 
        Normalised image data within the range [p_min, p_max].
    
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