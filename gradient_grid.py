import numpy as np
import matplotlib.pyplot as plt
import math

def gauss_grid(size_x, size_y=None):

    if size_y == None:
        size_y = size_x
    sigma_x = 0.17 * size_x
    sigma_y = 0.17   * size_y

    assert isinstance(size_x, int)
    assert isinstance(size_y, int)

    x0 = size_x // 2
    y0 = size_y // 2

    x = np.arange(0, size_x, dtype=float)
    y = np.arange(0, size_y, dtype=float)[:,np.newaxis]

    x -= x0
    y -= y0

    exp_part = x**2/(2*sigma_x**2)+ y**2/(2*sigma_y**2)
    dist = 1/(2*np.pi*sigma_x*sigma_y) * np.exp(-exp_part)
    return dist * (256/dist.max())

def alpha_gradient_grid( size_x, size_y=None, color="#888888", alpha=0.1 ):
    arr = []
    for row in gauss_grid( size_x, size_y ).tolist():
        for item in row:
            arr.append( "{}{:02X}".format( color, math.floor( alpha * item ) ) )
    return arr
