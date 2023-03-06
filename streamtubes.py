from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
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

    seeds = vtkPlaneSource()
    seeds.SetResolution(8, 8)

    trans = vtkTransform()
    trans.RotateY(90)
    trans.Scale(0.5, 1, 1)
    trans.Translate(0.3, 0, 0)

    tpd_filter = vtkTransformPolyDataFilter()
    tpd_filter.SetInputConnection(seeds.GetOutputPort())
    tpd_filter.SetTransform(trans)

    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(vfem_filename)

    streamline = vtkStreamTracer()
    streamline.SetSourceConnection(tpd_filter.GetOutputPort())
    streamline.SetInputConnection(reader.GetOutputPort())

    tube = vtkTubeFilter()
    tube.SetInputConnection(streamline.GetOutputPort())
    tube.SetRadius(0.01)
    tube.Update()
    tube_range: tuple[float, float] = streamline.GetOutput().GetScalarRange()

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(tube.GetOutputPort())
    mapper.SetScalarRange(tube_range)

    actor = vtkActor()
    actor.SetMapper(mapper)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(mapper.GetLookupTable())  # type: ignore

    build_window([actor, build_wing_actor(args.wing)], [scalar_bar]).Start()


if __name__ == "__main__":
    main()
