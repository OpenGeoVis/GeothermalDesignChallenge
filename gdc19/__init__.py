"""This Python package holds a whole lot of utilities developed for the 2019
Utah FORGE Geothermal Design Challenge
"""

DATA_DIRECTORY = None

from gdc19.path import *
from gdc19.surfaces import *
from gdc19.textures import *
from gdc19.shapefiles import *
from gdc19.wells import *
from gdc19.project import *

# Project MetaData
__author__ = 'Bane Sullivan'
__license__ = 'Undecided'
__copyright__ = '2018-2019, Bane Sullivan'
__version__ = '0.0.0'
__displayname__ = '2019 Utah FORGE Geothermal Design Challenge'


# Save VTKjs files in a particular location
EXPORT_PATH = os.path.abspath('../vtkjs/')
if not os.path.exists(EXPORT_PATH):
    os.makedirs(EXPORT_PATH)
EXPORT_PATH = os.path.join(EXPORT_PATH, r'{}')


def setup():
    # Make consistent figures
    vtki.set_plot_theme('doc')
    vtki.rcParams['font']['size'] = 12
    vtki.rcParams['font']['title_size'] = 12
    vtki.rcParams['font']['label_size'] = 12
    vtki.rcParams['use_panel'] = False
    # Save figures in specified directory
    import os
    vtki.FIGURE_PATH = os.path.abspath('../images/')
    if not os.path.exists(vtki.FIGURE_PATH):
        os.makedirs(vtki.FIGURE_PATH)
    # Set up path to datafiles
    return set_data_directory('/Volumes/GoogleDrive/My Drive/utah-forge')

def setup_bane():
    return setup()

def setup_adam():
    return setup()

setup()
