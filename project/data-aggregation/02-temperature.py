"""
Temperature Data
~~~~~~~~~~~~~~~~

"""
# sphinx_gallery_thumbnail_number = 4
# Import project package
import gdc19

###############################################################################
import vtki
import PVGeo
import omf
import omfvtk
import pandas as pd
import numpy as np


###############################################################################
# Temperature Probe Data
# ++++++++++++++++++++++

# Load the temperature data
_temp = pd.read_csv(
            gdc19.get_temperature_path('well_based_temperature.csv')
            )
_temp.head()

###############################################################################
temperature = omf.PointSetElement(
    name='temperature',
    description='cumulative record of one-dimensional temperature modeling '\
        'based off of well data. Temperature log data were exampled and '\
        'extrapolated below the bottom of a number of wells. Temperatures '\
        'are in degrees Celsius, and all location data are georeferenced to '
        'UTM, zone 12N, NAD 83, NAVD 88.',
    subtype='point',
    geometry=omf.PointSetGeometry(
        vertices=_temp[['x', 'y', 'z']].values
    ),
    data=[omf.ScalarData(
        name='temperature (C)',
        array=_temp['T'].values,
        location='vertices'
    ),]
)
temperature.validate()


###############################################################################
temp = omfvtk.wrap(temperature)
temp.plot()


###############################################################################
# Geostatistical Model
# ++++++++++++++++++++
#
# Prep temperature data for kriging in SGeMS

# First, load the topography surface that was previously aggregated:
surfaces = omfvtk.load_project(gdc19.get_project_path('surfaces.omf'))
topo = surfaces['land_surface']


p = vtki.Plotter()
p.add_mesh(temp, cmap='coolwarm', point_size=10,
           render_points_as_spheres=True, stitle='Temperature')
p.add_mesh(topo)
p.camera_position = [1,1,-1]
p.show()

###############################################################################
# Make tables of the temperature and topography data

# Make pandas data frame of the temps
df_temp = pd.DataFrame(data=np.c_[temp.points, temp.point_arrays['temperature (C)']],
                    columns=['x', 'y', 'z', 'temp_c'])
df_temp.header = 'temperature (degrees C)'
print(df_temp.head())

###############################################################################

# And of the topography surface
df_topo = pd.DataFrame(data=topo.points, columns=['x','y','z'])
df_topo.header = 'Land Surface'
print(df_topo.head())

###############################################################################
# Save these tabular data frames to GSLib formatted files for use in SGeMS

gdc19.save_gslib(gdc19.get_krig_path('temperature.gslib'), df_temp)
gdc19.save_gslib(gdc19.get_krig_path('topography.gslib'), df_topo)

###############################################################################
# Load the kriged temperature model from SGeMS

fkrig = gdc19.get_krig_path("Geotherm_kriged_0.sgems")
fvar = gdc19.get_krig_path("Geotherm_kriged_0_krig_var.sgems")

# Read the kirgged model and variance
grid = PVGeo.gslib.SGeMSGridReader().apply(fkrig)
grid_var = PVGeo.gslib.SGeMSGridReader().apply(fvar)

# Label the array appropriately
grid.rename_scalar('Getherm_kriged_0', 'Temperature')
grid.cell_arrays['Temperature_var'] = grid_var.cell_arrays['Getherm_kriged_0_krig_var']

###############################################################################
# Set the spatial reference of the grid
# Values from SGeMS:
grid.origin = (325000, 4.245e6, -2700)
grid.spacing = (250, 250, 50)

grid.plot(cmap='coolwarm')

###############################################################################
# Lets quickly inspect the model

bounds = gdc19.get_roi_bounds()
clipped = grid.clip_box(bounds, invert=False)

contours = clipped.cell_data_to_point_data().contour()
contours.plot(cmap='coolwarm', clim=clipped.get_data_range())


###############################################################################
#  Now we need to convert the model to the OMF files specification

# MINUS ONE BECASE WE DEFINE CELL DATA
ncx, ncy, ncz = np.array(grid.dimensions) - 1
sx, sy, sz = grid.spacing


temp_model = omf.VolumeElement(
        name='kriged_temperature_model',
        description='kriged temoerature model built from temperature probe data',
        geometry=omf.VolumeGridGeometry(
            tensor_u=np.full(ncx, sx),
            tensor_v=np.full(ncy, sy),
            tensor_w=np.full(ncz, sz),
            origin=grid.origin,
        ),
        data=[omf.ScalarData(
                name='temperature (C)',
                array=grid.cell_arrays['Temperature'].reshape((ncz,ncy,ncx), order='F').ravel(),
                location='cells'),
              omf.ScalarData(
                name='Temperature_var',
                array=grid.cell_arrays['Temperature_var'].reshape((ncz,ncy,ncx), order='F').ravel(),
                location='cells'),
             ],
)
temp_model.validate()

###############################################################################
# And one final sanity check

omfvtk.wrap(temp_model).clip_box(gdc19.get_roi_bounds(), invert=False).plot(cmap='coolwarm')


###############################################################################
# Write the data
# ++++++++++++++

proj = omf.Project(
    name='FORGE Temperature Data',
    description='All temperature data/models for the 2019 FORGE Geothermal Student Competition '
)

proj.elements = [ temperature,  temp_model]

proj.validate()

###############################################################################
# Save the temperature project file

omf.OMFWriter(proj, gdc19.get_project_path('temperature.omf'))
