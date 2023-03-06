from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
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
    seeds.SetResolution(15, 15)
    seeds.SetNormal(1, 0, 0)

    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(vfem_filename)

    streamline = vtkStreamTracer()
    streamline.SetSourceConnection(seeds.GetOutputPort())
    streamline.SetInputConnection(reader.GetOutputPort())
    streamline.Update()
    streamline_range: tuple[float, float] = streamline.GetOutput().GetScalarRange()

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(streamline.GetOutputPort())
    mapper.SetScalarRange(streamline_range)

    actor = vtkActor()
    actor.SetMapper(mapper)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(mapper.GetLookupTable())  # type: ignore

    build_window([actor, build_wing_actor(args.wing)], [scalar_bar]).Start()


if __name__ == "__main__":
    main()
