import shapefile
import numpy as np
import omf

import vtk
import vtki

# sklearn's KDTree is fast: use it if available
from sklearn.neighbors import KDTree as Tree


def _fix_to_topography(topo_points, points_to_update, static=20.0):
    """Update the z component of points to force them to lie on a topo surface"""
    tree = Tree(topo_points)
    ind = tree.query(points_to_update, k=1)[1].ravel()
    # Now update the elevation to be on the topo surface
    # Also shift it so its always just above the surface and not in the surface
    points_to_update[:,2] = topo_points[:,2][ind] + static
    return points_to_update


def _makeLineCell(idx0, idx1):
    """Create a vtkLine cell"""
    aLine = vtk.vtkLine()
    aLine.GetPointIds().SetId(0, idx0)
    aLine.GetPointIds().SetId(1, idx1)
    return aLine

def polygon_to_vtk(polygon, topo_points):
    """Converts a polygon shape to a vtki.PolyData object.
    This assumes the points are ordered.
    """
    pts = np.array(polygon.points)
    pts = np.c_[pts, np.zeros(pts.shape[0])]
    pts = _fix_to_topography(topo_points, pts)
    cells = vtk.vtkCellArray()
    for i in range(pts.shape[0]-1):
        cell = _makeLineCell(i, i+1)
        cells.InsertNextCell(cell)
    # Add in last connection to make complete polygon
    cell = _makeLineCell(i, 0)
    cells.InsertNextCell(cell)
    # Build the output
    pdo = vtk.vtkPolyData()
    pdo.SetPoints(vtki.vtk_points(pts))
    pdo.SetLines(cells)
    return vtki.wrap(pdo)


def polygon_to_omf(polygon, topo_points, description='Line set polygon', name='polygon'):
    """Converts a polygon shape to an OMF.LineSetElement object.
    This assumes the points are ordered.
    """
    pts = np.array(polygon.points)
    pts = np.c_[pts, np.zeros(pts.shape[0])]
    pts = _fix_to_topography(topo_points, pts)
    partial = np.arange(0, pts.shape[0], dtype=int)
    segments = np.c_[partial, np.roll(partial, -1)]
    element = omf.LineSetElement(
        name=name,
        description=description,
        subtype='line',
        geometry=omf.LineSetGeometry(
            vertices=pts,
            segments=segments,
        )
    )
    return element



VTK_CONVERTERS = {
    shapefile.POLYGON: polygon_to_vtk,
}

def read_shape_file_to_vtk(filename, topo_points):
    """Read all the features of a shapefile into vtki objects.
    Use the topo_points argument to fill the Z component of 2D points
    """
    shp = shapefile.Reader(filename)
    output = vtki.MultiBlock()
    for i, feature in enumerate(shp.shapeRecords()):
        shape = feature.shape
        try:
            output[i, feature.record[1]] = VTK_CONVERTERS[shape.shapeType](shape, topo_points)
        except KeyError:
            raise RuntimeError('Shape type ({}) unknown'.format(shape.shapeType))
    return output


OMF_CONVERTERS = {
    shapefile.POLYGON: polygon_to_omf,
}

def read_shape_file_to_omf(filename, topo_points):
    """Read all the features of a shapefile into OMF objects.
    Use the topo_points argument to fill the Z component of 2D points
    """
    shp = shapefile.Reader(filename)
    elements = []
    for i, feature in enumerate(shp.shapeRecords()):
        shape = feature.shape
        try:
            elements.append(OMF_CONVERTERS[shape.shapeType](shape, topo_points))
        except KeyError:
            raise RuntimeError('Shape type ({}) unknown'.format(shape.shapeType))
    return elements
