from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.build_seeds_around_vortices import build_source_around_vortices
from src.build_velocity_actor import build_velocity_actor
from src.build_window import build_window
from src.build_wing_actor import build_wing_actor
from src.parse_args import parse_args
from src.read_vfem_velocity import read_vfem_velocity
from src.vtk_side_effects import import_for_rendering_core


def main():
    import_for_rendering_core()
    args = parse_args()

    wing_filename = args.wing
    vfem_filename = args.vfem

    seeds = vtkPlaneSource()
    seeds.SetResolution(15, 15)
    seeds.SetNormal(1, 0, 0)

    reader, velocity_range = read_vfem_velocity(vfem_filename)

    source = build_source_around_vortices(n_seeds=50)

    streamline = vtkStreamTracer()
    streamline.SetSourceConnection(source.GetOutputPort())
    streamline.SetInputConnection(reader.GetOutputPort())

    streamline_actor, _ = build_velocity_actor(
        streamline.GetOutputPort(), velocity_range
    )

    contour_range = [40900.0, 43721.0]

    contour = vtkContourFilter()
    contour.SetInputConnection(reader.GetOutputPort())
    contour.GenerateValues(8, contour_range)

    contour_mapper = vtkDataSetMapper()
    contour_mapper.SetInputConnection(contour.GetOutputPort())
    contour_mapper.SetScalarRange(contour_range)

    contour_actor = vtkActor()
    contour_actor.SetMapper(contour_mapper)
    contour_actor.GetProperty().SetOpacity(0.25)

    build_window(
        [build_wing_actor(wing_filename), streamline_actor, contour_actor],
        [],
        depth_peeling=True,
    ).Start()


if __name__ == "__main__":
    main()
