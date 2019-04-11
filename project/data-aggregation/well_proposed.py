"""
Proposed Well
-------------
"""

import sys
# This makes the gdc19 package avaialble
sys.path.append('../../')
import gdc19

###############################################################################
import numpy as np
import vtki


###############################################################################

# GET THE WELLS DATABASE
WELLS = gdc19.load_well_db()


###############################################################################
# Proposed Well 1
# ~~~~~~~~~~~~~~~
#
# Coordinates: x = 335103.383, y = 4261756, z = 1700
#
# Depth: 2200 m

depth = 2200
start_x = 335230.383
start_y = 4261710
start_z = 1698

WELLS['well_new1'] = gdc19.build_well_trajectory(depth, start_x, start_y, start_z)


###############################################################################
# Proposed Well 2
# ~~~~~~~~~~~~~~~
#
# Coordinates: x = 336000	, y = 4263240.829,  z = 1700
#
# Depth: 2200 m


depth = 2200
start_x = 334618
start_y = 4262018
start_z = 1665

WELLS['well_new2'] = gdc19.build_well_trajectory(depth, start_x, start_y, start_z)


gdc19.save_well_db(WELLS)
