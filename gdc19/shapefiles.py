import shapefile
import numpy as np

import vtk
import vtki


def _makeLineCell(idx0, idx1):
    """Create a vtkLine cell"""
    aLine = vtk.vtkLine()
    aLine.GetPointIds().SetId(0, idx0)
    aLine.GetPointIds().SetId(1, idx1)
    return aLine

def polygon_to_vtk(ploygon, z_fill):
    """Converts a polygon shape to a vtki.PolyData object.
    This assumes the points are ordered.
    """
    pts = np.array(ploygon.points)
    pts = np.c_[pts, np.full(pts.shape[0], z_fill)]
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



CONVERTERS = {
    shapefile.POLYGON: polygon_to_vtk,
}

def read_shape_file(filename, z_fill=0.0):
    """Read all the features of a shapefile into vtki objects.
    Use the z_fill argument to fill the Z component of 2D points
    """
    shp = shapefile.Reader(filename)
    output = vtki.MultiBlock()
    for i, feature in enumerate(shp.shapeRecords()):
        shape = feature.shape
        try:
            output[i, feature.record[1]] = CONVERTERS[shape.shapeType](shape, z_fill)
        except KeyError:
            raise RuntimeError('Shape type ({}) unknown'.format(shape.shapeType))
    return output
