"""

GIS Data
~~~~~~~~

Convert all the GIS data to OMF

Be sure to install ``gdal``::

    conda install gdal

"""


# Import project package
import gdc19

###############################################################################

import vtki
import omf
import omfvtk
import pandas as pd
import numpy as np


###############################################################################
# First, get the land surface to match Z-coordinates of shape files with
# the topography.

description='vertices of meshed/interpolated surfaces of the ' \
    'land surface (based on 10-meter DEM) used in the Phase 2B '\
    'earth model. All data are georeferenced to UTM, zone 12N, '\
    'NAD 83, NAVD 88.'

land_surface = gdc19.surf_to_omf(
    'land_surface_vertices.csv',
    'land_surface',
    description
    )
land_surface.validate()
topo = omfvtk.wrap(land_surface)

###############################################################################
# Load the shape files
shapes = gdc19.read_shape_file_to_omf(
    gdc19.get_shp_path('FORGE_Outline'), topo_points=topo.points
)
shapes

###############################################################################

boundary = shapes[0]
boundary.name = 'boundary'
boundary.validate()

###############################################################################
omfvtk.wrap(boundary).plot(show_edges=False)


###############################################################################
# Now save out the GIS data to an OMF project file

proj = omf.Project(
    name='FORGE GIS Data',
    description='All GIS data for the 2019 FORGE Geothermal Student Competition '
)

proj.elements = [ boundary ]

proj.validate()

###############################################################################
# Save the GIS project file

omf.OMFWriter(proj, gdc19.get_project_path('gis.omf'))
