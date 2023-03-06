from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkProbeFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkPlaneSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.build_window import build_window
from src.build_wing_actor import build_wing_actor
from src.parse_args import parse_args
from src.vtk_side_effects import import_for_rendering_core


def main():
    import_for_rendering_core()
    args = parse_args()
    vfem_filename = args.vfem

    vfem_reader = vtkXMLUnstructuredGridReader()
    vfem_reader.SetFileName(vfem_filename)

    plane_x_coords = [0.05, 0.4, 0.6]
    arrow_actors = [
        build_arrow_plane_actor(vfem_reader.GetOutputPort(), x) for x in plane_x_coords
    ]

    build_window(
        [build_wing_actor(args.wing)] + arrow_actors,
        [],
    ).Start()


def build_arrow_plane_actor(reader_output_port: vtkAlgorithmOutput, x: float):
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
    probe_filter.SetSourceConnection(reader_output_port)

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

    arrow_actor = vtkActor()
    arrow_actor.SetMapper(arrow_mapper)
    return arrow_actor


if __name__ == "__main__":
    main()
