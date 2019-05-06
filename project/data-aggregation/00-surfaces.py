"""
Surface Data
~~~~~~~~~~~~

This notebook aggregates all the surface data for the FORGE site into a single
Open Mining Format (OMF) project file.

Here we load all the surface data and create `omf.SurfaceElement` objects.

"""
# sphinx_gallery_thumbnail_number = 6
# Import project package
import gdc19

###############################################################################
import vtki
import omf
import omfvtk
import pandas as pd
import numpy as np


###############################################################################
description='This contains vertices of meshed/interpolated ' \
    'surfaces of the granitoid-basin fill contact used in the ' \
    'Phase 2B earth model. All data are georeferenced to UTM, ' \
    'zone 12N, NAD 83, NAVD 88.'

top_granitoid = gdc19.surf_to_omf(
    'top_granitoid_vertices.csv',
    'top_granitoid',
    description
    )
top_granitoid.validate()

###############################################################################
omfvtk.wrap(top_granitoid).plot(show_edges=False)

###############################################################################
description='Negro Mag Fault used in the Phase 2B earth model. ' \
    'All data are georeferenced to UTM, zone 12N, NAD 83, NAVD 88.'

negro_mag_fault = gdc19.surf_to_omf(
    'Negro_Mag_Fault_vertices.csv',
    'negro_mag_fault',
    description
    )
negro_mag_fault.validate()
###############################################################################
omfvtk.wrap(negro_mag_fault).plot(show_edges=False)

###############################################################################

description='surfaces of the Opal Mound Fault used in the Phase ' \
    '2B earth model. All data are georeferenced to UTM, zone '\
    '12N, NAD 83, NAVD 88.'

opal_mound_fault = gdc19.surf_to_omf(
    'Opal_Mound_Fault_vertices.csv',
    'opal_mound_fault',
    description
    )
opal_mound_fault.validate()

###############################################################################
omfvtk.wrap(opal_mound_fault).plot(show_edges=False)

###############################################################################


# temp_175c: '175C_vertices.csv'
description='vertices of meshed/interpolated surfaces of the ' \
    'interpolated temperature isosurfaces for 175 degrees C used ' \
    'in the Phase 2B earth model. All data are georeferenced to ' \
    'UTM, zone 12N, NAD 83, NAVD 88.'

temp_175c = gdc19.surf_to_omf(
    '175C_vertices.csv',
    'temp_175c',
    description
    )
temp_175c.data = [
        omf.ScalarData(
            name='constant temperature value of 175 for surface',
            array=np.full(temp_175c.geometry.num_nodes, 175.),
            location='vertices'),]
temp_175c.validate()
###############################################################################

omfvtk.wrap(temp_175c).plot(show_edges=False)

###############################################################################

# temp_225c: '225C_vertices.csv'
description='vertices of meshed/interpolated surfaces of the '\
    'interpolated temperature isosurfaces for 225 degrees C used '\
    'in the Phase 2B earth model. All data are georeferenced to ' \
    'UTM, zone 12N, NAD 83, NAVD 88.'

temp_225c = gdc19.surf_to_omf(
    '225C_vertices.csv',
    'temp_225c',
    description
    )
temp_225c.data = [
        omf.ScalarData(
            name='constant temperature value of 225 for surface',
            array=np.full(temp_225c.geometry.num_nodes, 225.),
            location='vertices'),]
temp_225c.validate()


###############################################################################
omfvtk.wrap(temp_225c).plot(show_edges=False)


###############################################################################
# land_surface: 'land_surface_vertices.csv'
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

###############################################################################

# NOW ADD TEXTURES TO THE LAND SURFACE

fname = gdc19.get_gis_path('Geologic_map_on_air_photo.png')
name = 'geo_aer'
description = 'geologic map of the Utah FORGE site with aerial '\
    'imagery. All data are georeferenced to UTM, zone 12N, NAD '\
    '83, NAVD 88.'
geo_aer = gdc19.load_texture_to_omf(fname, name, description)

# topographic_map.png
fname = gdc19.get_gis_path('topographic_map.png')
name = 'topo_map'
description = ' topographic map of the Utah FORGE site. '\
    'All data are georeferenced to UTM, zone 12N, NAD 83, NAVD 88.'
topo_map = gdc19.load_texture_to_omf(fname, name, description)

# Geologic_map_no_quaternary.tif
fname = gdc19.get_gis_path('Geologic_map_no_quaternary.png')
name = 'geo_no_aer'
description = 'geologic map of the Utah FORGE site with '\
    'quaternary faults labeled. All data are georeferenced to UTM, '\
    'zone 12N, NAD 83, NAVD 88.'
geo_no_aer = gdc19.load_texture_to_omf(fname, name, description)

land_surface.textures = [geo_aer, topo_map, geo_no_aer]
land_surface.validate()

###############################################################################
topo = omfvtk.wrap(land_surface)

###############################################################################

topo.plot(show_edges=False, texture=True)

###############################################################################
# And now create an OMF project file for the surfaces

proj = omf.Project(
    name='FORGE Surfaces',
    description='All surfaces for the 2019 FORGE Geothermal Student Competition '
)

proj.elements = [land_surface,
                 temp_225c,
                 temp_175c,
                 opal_mound_fault,
                 negro_mag_fault,
                 top_granitoid,
                ]

proj.validate()

###############################################################################
# Save the GIS project file

omf.OMFWriter(proj, gdc19.get_project_path('surfaces.omf'))
