from PIL import Image
from ipywidgets import interact
from IPython.display import display
import warnings
import numpy as np
from numba import njit
from matplotlib.pyplot import get_cmap

@njit
def _colorim(x, colors):
    """Colors a grayscale image using a LUT
    
    Parameters
    ----------
    x : np.ndarray
        The image to be colored
    colors : np.ndarray
        The colors, ensure colors from 0 ... 255
    
    Returns
    -------
    np.ndarray (RGBA)
        The input image colored
    """
    im = np.zeros(x.shape+(4,), dtype=np.uint8)
    
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            im[i,j] = colors[x[i,j]]
            
    return im

def browse(x, axis=0, resize=None, enhance_contrast=True, antialiasing=False, cutoff_min=None, cutoff_max=None, cmap=None):
    """Browsing through an image stack seemlessly
    
    Parameters
    ----------
    x : np.ndarray
        An grayscale or RGB image and stack
    axis : int, optional
        browsing axis, by default 0
    resize : int, optional
        resize image by a factor, e.g. 2, by default None
    enhance_contrast : bool, optional
        enhance contrast of image using min/max, by default True
    antialiasing : bool, optional
        smooth image when resizing, by default False
    cutoff_min : int, optional
        clip minimum value, by default None
    cutoff_max : int, optional
        clip maximum value, by default None
    cmap: str, optional
        applies colormap to grayscale image, by default None
    
    Raises
    ------
    warning
        when float arrays are shown
    """
    s = x.shape
    
    assert type(axis) == int, "axis must be an interger"
    assert len(s) >= 2, "image must be at least 2D"
    
    # Can only show single images, no deeper inspection possible
    if axis > 0 and (len(s) == 2 or (len(s) == 3 and s[-1] == 3)):
        assert True, print("The array of shape {} cannot be browsed deeper".format(s))
        
    # Make single image a pseudo-stack
    if axis == 0 and (len(s) == 2 or (len(s) == 3 and s[-1] == 3)):
        x = x[None]
        s = x.shape
        
    # Normally use nearest neighbour interpolation
    RESIZE_FLAG = Image.NEAREST
    
    if antialiasing:
        RESIZE_FLAG = Image.ANTIALIAS

    if cmap:
        # Get cmap from matplotlib
        c = get_cmap(cmap)
        # Get colors from cmap and scale it from [0,1] to [0, 255]
        colors = np.array([np.array(c(i))*255 for i in np.linspace(0, 1, 256)], dtype=np.uint8)
    
    @interact
    def __(a:(0, s[axis]-1)):
        # Dynamic fancy indexing using axis as argument
        im = np.take(x, a, axis)
        
        # If data should be shown in a specific range
        if cutoff_min or cutoff_max:
            im = np.clip(im, cutoff_min, cutoff_max)
        
        # If data is a float numpy array,
        # raise warning and convert to uint8
        if im.dtype == np.float32 or im.dtype == np.float64 or im.dtype == np.float64:
            warnings.warn("Your dtype is {}, will be converted".format(im.dtype)+\
                "to uint8 for display purposes")
            im = im.astype(np.uint8)
        
        if enhance_contrast:
            im -= im.min()
            im = (im.astype(np.float32) / im.max() * 255).astype(np.uint8)

        # If grayscale image should be colored using a LUT
        if cmap and len(im.shape) == 2:
            im = _colorim(im, colors)
        
        # Convert numpy array to PIL Image
        im_pil = Image.fromarray(im)
        
        # If image is too small and people asked for resizing
        if resize is not None:
            w, h = im.shape[:2]
            im_pil = im_pil.resize((int(h*resize), 
                                    int(w*resize)), RESIZE_FLAG)
        
        # Show image
        display(im_pil)
