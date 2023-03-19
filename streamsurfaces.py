from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersFlowPaths import vtkStreamSurface
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkLineSource

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

    seeds = vtkLineSource()
    seeds.SetResolution(300)

    trans = vtkTransform()
    trans.RotateZ(90)
    trans.Scale(0.1, 1, 1)
    trans.Translate(0, 0, -0.015)

    tpd_filter = vtkTransformPolyDataFilter()
    tpd_filter.SetInputConnection(seeds.GetOutputPort())
    tpd_filter.SetTransform(trans)

    stream_surface = vtkStreamSurface()
    stream_surface.SetSourceConnection(tpd_filter.GetOutputPort())
    stream_surface.SetInputConnection(reader.GetOutputPort())

    actor, scalar_bar = build_velocity_actor(
        stream_surface.GetOutputPort(), velocity_range
    )

    actor.GetProperty().SetOpacity(0.5)

    build_window(
        [actor, build_wing_actor(args.wing)], [scalar_bar], depth_peeling=True
    ).Start()


if __name__ == "__main__":
    main()
