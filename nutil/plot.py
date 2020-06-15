import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

def paperStyle(font_size=8, use_seaborn=True):
    """Defines plot styles for paper

    Args:
        font_size (int, optional): Figure font size. Defaults to 8 (pt).
        use_seaborn (bool, optional): If seaborn is used to style the plot. Defaults to True.
    """    
    if use_seaborn:
        sns.set_style('white')
        sns.set_style('ticks')

    plt.rcParams['axes.labelsize'] = font_size
    plt.rcParams['xtick.labelsize'] = font_size
    plt.rcParams['ytick.labelsize'] = font_size
    plt.rcParams['legend.fontsize'] = font_size
    plt.rcParams['title.fontsize'] = font_size
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['svg.fonttype'] = 'none' # Text is not rendered
    plt.rcParams['pdf.fonttype'] = 42 # TrueType to avoid PDF issues
    

def grabFigure(fig, autoclose=True):
    """Grabs a figure to a numpy array

    Args:
        fig (matplotlib.figure): The figure reference
        autoclose (bool, optional): Close the figure automatically. Defaults to True.

    Returns:
        np.ndarray, the figure as RGB image numpy array
    """    
    fig.canvas.draw() 
    rgb = fig.canvas.tostring_rgb()
    shape = fig.canvas.get_width_height()[::-1] + (3,)
    
    if autoclose:
        plt.close(fig)
        
    # Returns numpy array
    return np.frombuffer(rgb, dtype=np.uint8).reshape(shape)
