import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import colour

def paperStyle(font_size=8, use_seaborn=True, temporary=True):
    """Defines plot styles for paper

    Args:
        font_size (int, optional): Figure font size. Defaults to 8 (pt).
        use_seaborn (bool, optional): If seaborn is used to style the plot. Defaults to True.
        temporary (bool, optional): Use `paperStyle` with `with` statement. Defaults to True.
    """    
    if use_seaborn:
        sns.set_style('white')
        sns.set_style('ticks')

    if temporary:
        return mpl.rc_context({
            'axes.labelsize': font_size,
            'xtick.labelsize': font_size,
            'ytick.labelsize': font_size,
            'legend.fontsize': font_size,
            'axes.titlesize': font_size,
            'font.family': ['sans-serif'],
            'font.sans-serif': ['Arial'],
            'svg.fonttype': 'none',
            'pdf.fonttype': 42

        })

    else:
        plt.rcParams['axes.labelsize'] = font_size
        plt.rcParams['xtick.labelsize'] = font_size
        plt.rcParams['ytick.labelsize'] = font_size
        plt.rcParams['legend.fontsize'] = font_size
        plt.rcParams['axes.titlesize'] = font_size
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

def lightSequential(target_color=(255, 165, 2), steps=256, reverse=False):
    """Creates a light sequential colormap for `matplotlib.imshow`

    Args:
        target_color (tuple or str, optional): Target color. Defaults to (255, 165, 2).
        steps (int, optional): Steps in colormaps, i.e. unique colors. Defaults to 256.
        reverse (bool, optional): Reverses colormap gradient. Defaults to False.

    Returns:
        ListedColormap: colormap with colors from white to target_color
    """
    if type(target_color) == str:
        tc = colour.Color(target_color)
        
    else:
        try:
            target_color = np.asarray(target_color, dtype=np.float32)
            
            if target_color.max() > 1:
                target_color /= 255
                
            tc = colour.Color(rgb=target_color)
            
        except Exception as e:
            print(e)
    
    
    colors = np.ones((steps, 4))
    base_l = float(tc.luminance)
    
    for i in range(1, steps+1):
        tc.luminance = base_l  + (1-base_l) * i/steps
        colors[i-1, :3] = tc.rgb

    return ListedColormap(colors[::-1] if reverse else colors)

def darkSequential(target_color=(255, 165, 2), steps=256, reverse=False):
    """Creates a dark sequential colormap for `matplotlib.imshow`

    Args:
        target_color (tuple or str, optional): Target color. Defaults to (255, 165, 2).
        steps (int, optional): Steps in colormaps, i.e. unique colors. Defaults to 256.
        reverse (bool, optional): Reverses colormap gradient. Defaults to False.

    Returns:
        ListedColormap: colormap with colors from black to target_color
    """
    if type(target_color) == str:
        tc = colour.Color(target_color)
        
    else:
        try:
            target_color = np.asarray(target_color, dtype=np.float32)
            
            if target_color.max() > 1:
                target_color /= 255
                
            tc = colour.Color(rgb=target_color)
            
        except Exception as e:
            print(e)
    
    colors = np.ones((steps, 4))
    base_l = float(tc.luminance)
    
    for i in range(1, steps+1):
        tc.luminance = base_l * i/steps
        colors[i-1, :3] = tc.rgb

    return ListedColormap(colors[::-1] if reverse else colors)