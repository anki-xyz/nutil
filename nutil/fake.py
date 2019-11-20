import numpy as np

def movingSquare(steps=10, shape=(200,200), factor=3):
    x = np.zeros((steps, ) + shape, dtype=np.float32)
    h = x.shape[1]//4
    w = x.shape[2]//4

    for i in range(steps):
        x[i, h+i*factor:2*h+i*factor,
        w+i*factor:2*w+i*factor] = 1

    return x