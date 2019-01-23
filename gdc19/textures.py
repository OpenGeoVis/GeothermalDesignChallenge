import gdal
import vtk
import vtki
import numpy as np

def get_point(gcp):
    return np.array([gcp.GCPX, gcp.GCPY, gcp.GCPZ])

def load_attach_texture(dataset, filename, name):
    """Loads a texture and attaches it to the dataset inplace.
    """
    # Load a raster
    ds = gdal.Open(filename)
    texture = vtki.load_texture(filename)
    # Grab the Groung Control Points
    points = [get_point(gcp) for gcp in ds.GetGCPs()]
    # Now Grab the three corners of their bounding box
    #-- This guarantees we grab the right points
    bounds = vtki.PolyData(np.array(points)).bounds
    origin = [bounds[0], bounds[2], bounds[4]] # BOTTOM LEFT CORNER
    point_u = [bounds[1], bounds[2], bounds[4]] # BOTTOM RIGHT CORNER
    point_v = [bounds[0], bounds[3], bounds[4]] # TOP LEFT CORNER
    dataset.texture_map_to_plane(origin, point_u, point_v, inplace=True, name=name)
    dataset.textures[name] = texture
    return None # No return because it updates input object inplace
