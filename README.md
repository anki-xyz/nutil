# nutil

Lazy functions for Jupyter notebooks

Installing:

    pip install git+https://github.com/anki-xyz/nutil

## Browsing

Fast image browsing based on PIL and IPython display.

Usage:

    import numpy as np
    from nutil import browse

    x = np.random.randint(0, 255, (10, 200, 200))

    browse(x, cmap='viridis')

![Browse through random stack](browse_example.gif)
