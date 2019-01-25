import gdal
import vtk
import vtki
import numpy as np
import omf
import properties

import gdc19

def get_point(gcp):
    return np.array([gcp.GCPX, gcp.GCPY, gcp.GCPZ])


def load_texture_to_omf(filename, name, description):
    """Loads a PNG Image texture to an ``omf.ImageTexture`` object"""
    # Load a raster
    ds = gdal.Open(filename.replace('.png', '.tif'))
    # Grab the Groung Control Points
    points = np.array([get_point(gcp) for gcp in ds.GetGCPs()])
    if points.size < 1:
        raise RuntimeError('No associated tif file to recover spatial reference.')
    # Now Grab the three corners of their bounding box
    #-- This guarantees we grab the right points
    bounds = vtki.PolyData(points).bounds
    origin = np.array([bounds[0], bounds[2], bounds[4]]) # BOTTOM LEFT CORNER
    point_u = np.array([bounds[1], bounds[2], bounds[4]]) # BOTTOM RIGHT CORNER
    point_v = np.array([bounds[0], bounds[3], bounds[4]]) # TOP LEFT CORNER
    axis_u = point_u - origin
    axis_v = point_v - origin
    the_texture = omf.ImageTexture(
        origin=origin,
        axis_u=axis_u, axis_v=axis_v,
        name=name, description=description,
        image=filename,
    )
    return the_texture

def load_attach_texture(dataset, filename, name):
    """Loads a texture and attaches it to the dataset inplace.
    """
    # Load a raster
    ds = gdal.Open(filename)
    texture = vtki.load_texture(filename)
    # Grab the Groung Control Points
    points = np.array([get_point(gcp) for gcp in ds.GetGCPs()])
    # Now Grab the three corners of their bounding box
    #-- This guarantees we grab the right points
    bounds = vtki.PolyData(points).bounds
    origin = [bounds[0], bounds[2], bounds[4]] # BOTTOM LEFT CORNER
    point_u = [bounds[1], bounds[2], bounds[4]] # BOTTOM RIGHT CORNER
    point_v = [bounds[0], bounds[3], bounds[4]] # TOP LEFT CORNER
    dataset.texture_map_to_plane(origin, point_u, point_v, inplace=True, name=name)
    dataset.textures[name] = texture
    return None # No return because it updates input object inplace


def attach_all_textures(dataset):
    """A helper to attach all the textures to a dataset"""
    names = ['geo_aer', 'topo_map', 'geo_no_aer']
    filenames = [
        gdc19.get_gis_path('Geologic_map_on_air_photo.tif'),
        gdc19.get_gis_path('topographic_map.tif'),
        gdc19.get_gis_path('Geologic_map_no_quaternary.tif'),
    ]
    for i in range(3):
        load_attach_texture(dataset, filenames[i], names[i])
    return None # No return because it updates input object inplace
