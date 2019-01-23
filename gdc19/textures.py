import gdal
import vtk
import vtki
import numpy as np

def get_point(gcp):
    return np.array([gcp.GCPX, gcp.GCPY, gcp.GCPZ])

def load_texture(filename):
    """Loads a texture and a ready to go vtk.TextureMapper.
    Be sure to set the input data object to the mapper and update it.
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
    # Map the plane
    m = vtk.vtkTextureMapToPlane()
    m.SetOrigin(origin) # BOTTOM LEFT CORNER
    m.SetPoint1(point_u) # BOTTOM RIGHT CORNER
    m.SetPoint2(point_v) # TOP LEFT CORNER
    # Return ready to use
    return texture, m

def attach_texture(dataset, texture, mapper, name):
    mapper.SetInputDataObject(dataset)
    mapper.Update()
    tmp = vtki.wrap(mapper.GetOutputDataObject(0))
    # Add these coordinates to the PointData of the dataset
    dataset.point_arrays[name] = tmp.t_coords
    # And associate the texture
    dataset.textures[name] = texture
    return None # No return because it updates input object

def load_attach_texture(dataset, filename, name):
    t, m = load_texture(filename)
    attach_texture(dataset, t, m, name)
    
