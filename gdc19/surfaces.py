import PVGeo
import vtki
import vtk
import numpy as np
import pandas as pd
import omf

import gdc19


def grid_surface(points):
    """Inserts structured points onto a grid
    and adds an elevation filter
    """
    points[:, 1] = points[::-1, 1]
    xu = np.unique(points[:, 0])
    yu = np.unique(points[:, 1])
    xx, yy = np.meshgrid(xu, yu)
    zz = points[:, 2].reshape(xx.shape)
    zz = np.flip(zz, axis=0)
    # Remove the last row because this is buggy
    xx = xx[0:-2, :]
    yy = yy[0:-2, :]
    zz = zz[0:-2, :]
    return vtki.StructuredGrid(xx, yy, zz).elevation()

def read_surface_verts(filename, grid=False):
    surf = pd.read_csv(filename)
    if grid:
        return grid_surface(surf.values)
    return PVGeo.pointsToPolyData(surf.values)


def delauney(polydata):
    """Run a delauney filter on a dataset"""
    alg = vtk.vtkDelaunay2D()
    alg.SetProjectionPlaneMode(vtk.VTK_BEST_FITTING_PLANE)
    alg.SetInputDataObject(polydata)
    alg.Update()
    return vtki.wrap(alg.GetOutputDataObject(0))


def surf_to_omf(filename, name, description, elevation=False):
    surf = delauney(
            read_surface_verts(
            gdc19.get_surfaces_path(filename)))
    if elevation:
        surf = surf.elevation()

    tris = surf.faces.reshape(surf.n_cells, 4)[:, 1:4]
    element = omf.SurfaceElement(
        name=name,
        description=description,
        geometry=omf.SurfaceGeometry(vertices=surf.points,
                                     triangles=tris)
        )
    element.validate()
    return element
