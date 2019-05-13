import datetime
import pyvista
import omf
import omfvista
import pandas as pd
import PVGeo
import warnings

import gdc19


def get_roi_bounds():
    """The ROI. Note Z-range is bigger than needed"""
    return [329924.98816, 344152.930125, 4252833.48213, 4270951.09811, -5000.0, 5000.0]


def load_project():
    return omfvista.load_project(gdc19.get_omf_project_filename())


def load_topo():
    proj = omf.OMFReader(gdc19.get_omf_project_filename()).get_project()
    for el in proj.elements:
        if el.name == 'land_surface':
            return omfvista.wrap(el)
    raise RuntimeError('Topo is not in project file. Some one messed up.')


def load_kriged_temp(clip=True):
    """Load the kriged temperature model from Lane Boyd"""
    fkrig = gdc19.get_krig_path("Geotherm_kriged_0.sgems")
    fvar = gdc19.get_krig_path("Geotherm_kriged_0_krig_var.sgems")
    # Read the kirgged model and variance
    grid = PVGeo.gslib.SGeMSGridReader().apply(fkrig)
    grid_var = PVGeo.gslib.SGeMSGridReader().apply(fvar)
    grid.rename_scalar('Getherm_kriged_0', 'Temperature')
    grid.cell_arrays['Temperature_var'] = grid_var.cell_arrays['Getherm_kriged_0_krig_var']
    # FROM SGeMS:
    grid.origin = (325000, 4.245e6, -2700)
    grid.spacing = (250, 250, 50)
    if clip:
        bounds = get_roi_bounds()
        grid = grid.clip_box(bounds, invert=False)
    return grid


def save_gslib(filename, dataframe, header=None):
    """This will save a pandas dataframe to a GSLib file"""
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('This can only save Pandas dataframes to GSLib files.')
    if header is None:
        try:
            header = dataframe.header
        except AttributeError:
            warnings.warn('Header not defined. Using date')
            header = str(datetime.datetime.now())
    if '\n' in header:
        raise RuntimeError('`header` can only be 1 line.')
    datanames = '\n'.join(dataframe.columns)
    with open(filename, 'w') as f:
        f.write('%s\n' % header)
        f.write('%d\n' % len(dataframe.columns))
        f.write(datanames)
        f.write('\n')
        dataframe.to_csv(f, sep=' ', header=None, index=False, float_format='%.9e')
    return 1
