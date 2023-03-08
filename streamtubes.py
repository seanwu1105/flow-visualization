from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer

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
    vfem_filename = args.vfem

    reader, velocity_range = read_vfem_velocity(vfem_filename)

    source = build_source_around_vortices(10)

    streamline = vtkStreamTracer()
    streamline.SetSourceConnection(source.GetOutputPort())
    streamline.SetInputConnection(reader.GetOutputPort())

    tube = vtkTubeFilter()
    tube.SetInputConnection(streamline.GetOutputPort())
    tube.SetRadius(0.005)

    actor, scalar_bar = build_velocity_actor(tube.GetOutputPort(), velocity_range)

    build_window([actor, build_wing_actor(args.wing)], [scalar_bar]).Start()


if __name__ == "__main__":
    main()
