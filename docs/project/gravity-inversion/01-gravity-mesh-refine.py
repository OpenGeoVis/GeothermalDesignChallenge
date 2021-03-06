"""
Creating an Inversion Mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~

This creates a mesh for inverting the gravity data.
"""
# sphinx_gallery_thumbnail_number = 2
import gdc19

import numpy as np
from discretize import TreeMesh
from discretize.utils import meshutils
import omfvista
from SimPEG.Utils import mkvc, modelutils
import pyvista


###############################################################################
# Load the Data
# +++++++++++++

# Load the topography surface that was previously aggregated:
surfaces = omfvista.load_project(gdc19.get_project_path('surfaces.omf'))
surface = surfaces['land_surface']
surface = surface.elevation()
surface.set_active_scalar('Elevation')
# Get the topography XYZ points
topo = surface.points

###############################################################################
# Load the gravity data
grav_data = pyvista.read(gdc19.get_gravity_path('grav_obs.vtk'))
xyz = grav_data.points
survey = pyvista.PolyData(xyz)

###############################################################################
# Visualize the survey on the topo
plotter = pyvista.Plotter()
plotter.add_mesh(surface, color='grey')
plotter.add_mesh(survey, color='k', point_size=5)
plotter.show()

###############################################################################
# Create a Mesh and Refine
# ++++++++++++++++++++++++

def compute_bounds(bounds, factor):
    # Define a region of interest
    bounds = list(bounds) # COPY IT
    delta = np.array([np.abs(bounds[1] - bounds[0]),
                      np.abs(bounds[3] - bounds[2]),
                      np.abs(bounds[5] - bounds[4])])
    cushion = delta * factor
    bounds[::2] += cushion
    bounds[1::2] -= cushion
    return bounds

bounds = compute_bounds(surface.bounds, 0.1)
print(bounds)

###############################################################################

# Create a mesh based on data extent
h = [40, 40, 20]
pads = [[0, 0], [0, 0],[2000, 0]]
octreeTopo = [0,5,10,10]
octreeObs = [5, 5]
maxDist = 100
depth_core = 2500

mesh = meshutils.mesh_builder_xyz(
    topo, h,
    padding_distance=pads,
    mesh_type='TREE',
    depth_core=depth_core,
)

mesh = meshutils.refine_tree_xyz(mesh, topo,
                                 octree_levels=octreeTopo,
                                 method='surface', finalize=False)

mesh = meshutils.refine_tree_xyz(mesh, xyz,
                                 octree_levels=octreeObs,
                                 method='surface',
                                 max_distance=maxDist,
                                 finalize=True)

actv = modelutils.surface2ind_topo(mesh, topo, gridLoc='N')

###############################################################################

def plot_pyvista(mesh, model, actv, interactive=False, use_panel=True, clim=None):
    # Convert TreeMesh to VTK
    dataset = mesh.toVTK()
    dataset.cell_arrays['Magnitude'] = model
    dataset.cell_arrays['Active'] = actv#np.load('active.npy').astype(int)
    dataset.active_scalar_name = 'Magnitude'

    # Remove inactive cells
    threshed = dataset.threshold(0.5, scalars='Active')

    # Instantiate plotting window
    plotter = pyvista.Plotter(notebook=not interactive)
    # Show axes labels
    plotter.show_grid(all_edges=False,)
    # Add a bounding box of original mesh to see total extent
    plotter.add_mesh(dataset.outline(), color='k')
    # Show input surface topography
    rng = list(surface.get_data_range())
    rng[0] -= (rng[1] - rng[0])/1.5
#     plotter.add_mesh(surface, cmap='gist_earth', clim=rng, opacity=.65)

    # Plotting params
    d_params = dict(
            show_edges=False,
            cmap='jet',
            scalars='Magnitude',
            scalar_bar_args=dict(label_font_size=20, title_font_size=25),
            clim=clim
        )

    # Clip volume in half
    plotter.add_mesh(threshed.clip('-y'), **d_params)

    # Add all the slices
    slices = threshed.slice_along_axis(n=5, axis='x')
    plotter.add_mesh(slices, name='slices', **d_params)

    # Show the mesh resolution at the surface
#     plotter.add_mesh(dataset.wireframe(), opacity=0.5, **d_params)
    # Add the vectors
    plotter.camera_position = [-1,-1,1]
    return plotter.show()

plot_pyvista(mesh, np.log10(mesh.vol), actv, False, False)

###############################################################################
# Save the mesh for use in an inversion

model_fname = gdc19.get_gravity_path('actv.mod')
mesh.writeUBC(gdc19.get_gravity_path('mesh.msh'), {model_fname:actv})
