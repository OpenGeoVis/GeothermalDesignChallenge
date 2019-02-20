import vtki
import omfvtk

import gdc19


def load_project():
    return omfvtk.load_project(gdc19.get_omf_project_filename())
