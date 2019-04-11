"""
Temperature Data
~~~~~~~~~~~~~~~~

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
omfvtk.wrap(temperature).plot(show_edges=False)
