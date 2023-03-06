from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkProbeFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkPlaneSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader, vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from src.parse_args import parse_args
from src.vtk_side_effects import import_for_rendering_core


def main():
    import_for_rendering_core()
    args = parse_args()
    vfem_filename = args.vfem
    wing_filename = args.wing

    wing_reader = vtkXMLPolyDataReader()
    wing_reader.SetFileName(wing_filename)

    wing_mapper = vtkDataSetMapper()
    wing_mapper.SetInputConnection(wing_reader.GetOutputPort())

    wing_actor = vtkActor()
    wing_actor.SetMapper(wing_mapper)

    vfem_reader = vtkXMLUnstructuredGridReader()
    vfem_reader.SetFileName(vfem_filename)

    plane_x_coords = [0.05, 0.4, 0.6]

    renderer = vtkRenderer()

    for x in plane_x_coords:
        renderer.AddActor(build_arrow_plane_actor(vfem_reader, x))

    renderer.AddActor(wing_actor)
    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("Gray"))  # type: ignore

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(640, 480)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Start()


def build_arrow_plane_actor(reader: vtkXMLUnstructuredGridReader, x: float):
    plane = vtkPlaneSource()
    plane.SetResolution(40, 40)

    trans = vtkTransform()
    trans.Translate(x, 0, 0)
    trans.RotateY(90)

    tpd_filter = vtkTransformPolyDataFilter()
    tpd_filter.SetInputConnection(plane.GetOutputPort())
    tpd_filter.SetTransform(trans)

    probe_filter = vtkProbeFilter()
    probe_filter.SetInputConnection(tpd_filter.GetOutputPort())
    probe_filter.SetSourceConnection(reader.GetOutputPort())

    arrow_source = vtkArrowSource()
    arrow_source.SetShaftResolution(20)
    arrow_source.SetTipResolution(20)
    arrow_source.SetShaftRadius(0.02)
    arrow_source.SetTipRadius(0.1)

    arrow_glyph_filter = vtkGlyph3D()
    arrow_glyph_filter.SetScaleFactor(0.000001)
    arrow_glyph_filter.SetInputConnection(probe_filter.GetOutputPort())
    arrow_glyph_filter.SetSourceConnection(arrow_source.GetOutputPort())

    arrow_mapper = vtkDataSetMapper()
    arrow_mapper.SetInputConnection(arrow_glyph_filter.GetOutputPort())
    arrow_mapper.SetScalarRange(reader.GetOutput().GetScalarRange())  # type: ignore

    arrow_actor = vtkActor()
    arrow_actor.SetMapper(arrow_mapper)
    return arrow_actor


if __name__ == "__main__":
    main()
