"""This Python package holds a whole lot of utilities developed for the 2019
Utah FORGE Geothermal Design Challenge
"""

DATA_DIRECTORY = None

from gdc19.path import *
from gdc19.surfaces import *
from gdc19.textures import *
from gdc19.shapefiles import *

# Project MetaData
__author__ = 'Bane Sullivan'
__license__ = 'Undecided'
__copyright__ = '2018, Bane Sullivan'
__version__ = '0.0.0'
__displayname__ = '2019 Utah FORGE Geothermal Design Challenge'


def setup():
    return set_data_directory('/Volumes/GoogleDrive/My Drive/utah-forge')

def setup_bane():
    return setup()

def setup_adam():
    return setup()
