from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersFlowPaths import vtkStreamSurface
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.build_window import build_window
from src.build_wing_actor import build_wing_actor
from src.parse_args import parse_args
from src.vtk_side_effects import import_for_rendering_core


def main():
    import_for_rendering_core()
    args = parse_args()
    vfem_filename = args.vfem

    seeds = vtkLineSource()

    trans = vtkTransform()
    trans.RotateY(90)

    tpd_filter = vtkTransformPolyDataFilter()
    tpd_filter.SetInputConnection(seeds.GetOutputPort())
    tpd_filter.SetTransform(trans)

    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(vfem_filename)

    stream_surface = vtkStreamSurface()
    stream_surface.SetSourceConnection(tpd_filter.GetOutputPort())
    stream_surface.SetInputConnection(reader.GetOutputPort())
    stream_surface.Update()
    stream_surface_range: tuple[
        float, float
    ] = stream_surface.GetOutput().GetScalarRange()

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(stream_surface.GetOutputPort())
    mapper.SetScalarRange(stream_surface_range)

    actor = vtkActor()
    actor.SetMapper(mapper)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(mapper.GetLookupTable())  # type: ignore

    build_window([actor, build_wing_actor(args.wing)], [scalar_bar]).Start()


if __name__ == "__main__":
    main()
