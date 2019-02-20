import numpy as np
import vtki

def build_well_trajectory(depth, start_x, start_y, start_z):
    r = np.arange(0.0, depth + 0.5, 0.5)
    phi = np.zeros(len(r))
    theta = np.zeros(len(r))

    for x in range(0, len(r)):
        theta[x] = -90

    #Well trajectory

    # get lengths of the separate segments
    r[1:] = r[1:] - r[:-1]
    # convert to radians
    phi = phi * 2 * np.pi / 360.
    theta = (90-theta) * 2 * np.pi / 360.
    # get x, y, z from known formulae
    x = start_x + (r*np.cos(phi)*np.sin(theta))
    y = start_y + (r*np.sin(phi)*np.sin(theta))
    z = (r*np.cos(theta))

    elevation = np.cumsum(z) + start_z
    return vtki.PolyData(np.c_[x,y,elevation])
