import vtki
import omf
import omfvtk
import PVGeo

import gdc19


def get_roi_bounds():
    """The ROI. Note Z-range is bigger than needed"""
    return [329924.98816, 344152.930125, 4252833.48213, 4270951.09811, -5000.0, 5000.0]


def load_project():
    return omfvtk.load_project(gdc19.get_omf_project_filename())


def load_kriged_temp(clip=True):
    """Load the kriged temperature model from Lane Boyd"""
    fkrig = gdc19.get_lane_path("geotherm-export/Geotherm_kriged_0.sgems")
    fvar = gdc19.get_lane_path("geotherm-export/Geotherm_kriged_0_krig_var.sgems")
    # Read the kirgged model and variance
    grid = PVGeo.gslib.SGeMSGridReader().Apply(fkrig)
    grid_var = PVGeo.gslib.SGeMSGridReader().Apply(fvar)
    grid.rename_scalar('Getherm_kriged_0', 'Temperature')
    grid.cell_arrays['Temperature_var'] = grid_var.cell_arrays['Getherm_kriged_0_krig_var']
    # FROM SGeMS:
    grid.origin = (325000, 4.245e6, -2700)
    grid.spacing = (250, 250, 50)
    if clip:
        bounds = get_roi_bounds()
        grid = grid.clip_box(bounds, invert=False)
    return grid
