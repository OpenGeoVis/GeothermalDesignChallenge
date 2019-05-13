"""
Surface Decimation
~~~~~~~~~~~~~~~~~~

Decimate some of the surfaces to make them more manageable with web renderings
in VTK.js
"""

import gdc19

import pandas as pd
import numpy as np
import pyvista
import omfvista
import PVGeo
import omf

###############################################################################

surfaces = omfvista.load_project(gdc19.get_project_path('surfaces.omf'))
topo = surfaces['land_surface']

###############################################################################
# Decimate Topography Surface

dec = topo.extract_geometry().decimate(0.99, inplace=False)
dec.plot(notebook=True, show_edges=True, color=True)

###############################################################################
# Re-do the texture mapping
reader = omf.OMFReader(gdc19.get_project_path('surfaces.omf'))
project = reader.get_project()
# Assumes 'land_surface' is at index 0
surf = project.elements[0]
tex = surf.textures[0]
print(tex.name)

og = tex.origin
pu = tex.axis_u
pv = tex.axis_v

dec.texture_map_to_plane(origin=og, point_u=og+pu, point_v=og+pv,
                          inplace=True, name='geo_aer')

dec.textures['geo_aer'] = pyvista.read_texture(gdc19.get_web_path('geology-aerial-compressed.jpg'))

dec.plot(texture=True)

dec.save(gdc19.get_web_path('topo.vtk'))


###############################################################################
# Decimate Granite Surface

gran = surfaces['top_granitoid']
print(gran)

###############################################################################
dec = gran.extract_geometry().decimate(0.99, inplace=False)
dec.plot(notebook=True, show_edges=True)

dec.save(gdc19.get_web_path('granite.vtk'))
