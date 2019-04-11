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
from gdc19.download import *

# Project MetaData
__author__ = 'Bane Sullivan'
__license__ = 'Undecided'
__copyright__ = '2018-2019, Bane Sullivan'
__version__ = '0.0.0'
__displayname__ = '2019 Utah FORGE Geothermal Design Challenge'


# Save VTKjs files in a particular location
EXPORT_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), '../vtkjs/')
if not os.path.exists(EXPORT_PATH):
    os.makedirs(EXPORT_PATH)
EXPORT_PATH = os.path.join(EXPORT_PATH, r'{}')


import appdirs
import os
USER_DATA_PATH = appdirs.user_data_dir('gdc19')
if not os.path.exists(USER_DATA_PATH):
    os.makedirs(USER_DATA_PATH)

# Make sure user has all the data
download_data()


def setup():
    # Make consistent figures
    vtki.set_plot_theme('doc')
    vtki.rcParams['font']['size'] = 12
    vtki.rcParams['font']['title_size'] = 12
    vtki.rcParams['font']['label_size'] = 12
    vtki.rcParams['use_panel'] = False
    # Save figures in specified directory
    vtki.FIGURE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), '../images/')
    if not os.path.exists(vtki.FIGURE_PATH):
        os.makedirs(vtki.FIGURE_PATH)
    # Set up path to datafiles
    # try:
    #     _ = os.environ['VTKI_OFF_SCREEN']
    #     travis = True
    # except KeyError
    #     travis = False
    # if travis:
    return

setup()
