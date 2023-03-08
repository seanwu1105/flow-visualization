from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPointSource


def build_source_around_vortices(n_seeds: int):
    seeds = vtkPointSource()
    seeds.SetRadius(0.05)
    seeds.SetNumberOfPoints(n_seeds)

    trans_0 = vtkTransform()
    trans_0.Translate(0, 0.05, -0.1)

    tpd_0 = vtkTransformPolyDataFilter()
    tpd_0.SetInputConnection(seeds.GetOutputPort())
    tpd_0.SetTransform(trans_0)

    trans_1 = vtkTransform()
    trans_1.Translate(0, -0.05, -0.1)

    tpd_1 = vtkTransformPolyDataFilter()
    tpd_1.SetInputConnection(seeds.GetOutputPort())
    tpd_1.SetTransform(trans_1)

    append_filter = vtkAppendPolyData()
    append_filter.AddInputConnection(tpd_0.GetOutputPort())
    append_filter.AddInputConnection(tpd_1.GetOutputPort())

    return append_filter
