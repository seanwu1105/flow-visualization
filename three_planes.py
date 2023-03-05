from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkProbeFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
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

import_for_rendering_core()
args = parse_args()
vfem_filename = args.vfem
wing_filename = args.wing

plane = vtkPlaneSource()
plane.SetResolution(40, 40)

trans = vtkTransform()
trans.Translate(0.5, 0, 0)
trans.RotateY(90)
trans.Scale(2, 2, 2)

tpd_filter = vtkTransformPolyDataFilter()
tpd_filter.SetInputConnection(plane.GetOutputPort())
tpd_filter.SetTransform(trans)

outline_filter = vtkOutlineFilter()
outline_filter.SetInputConnection(tpd_filter.GetOutputPort())

plane_mapper = vtkDataSetMapper()
plane_mapper.SetInputConnection(outline_filter.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(0, 0, 0)
plane_actor.GetProperty().SetLineWidth(1)

vfem_reader = vtkXMLUnstructuredGridReader()
vfem_reader.SetFileName(vfem_filename)
vfem_reader.Update()

probe_filter = vtkProbeFilter()
probe_filter.SetInputConnection(tpd_filter.GetOutputPort())
probe_filter.SetSourceConnection(vfem_reader.GetOutputPort())

arrow_source = vtkArrowSource()
arrow_source.SetShaftRadius(0.01)
arrow_source.SetTipRadius(0.02)

arrow_glyph_filter = vtkGlyph3D()
arrow_glyph_filter.SetScaleFactor(0.000005)
arrow_glyph_filter.SetInputConnection(probe_filter.GetOutputPort())
arrow_glyph_filter.SetSourceConnection(arrow_source.GetOutputPort())

arrow_mapper = vtkDataSetMapper()
arrow_mapper.SetInputConnection(arrow_glyph_filter.GetOutputPort())

arrow_actor = vtkActor()
arrow_actor.SetMapper(arrow_mapper)

wing_reader = vtkXMLPolyDataReader()
wing_reader.SetFileName(wing_filename)

wing_mapper = vtkDataSetMapper()
wing_mapper.SetInputConnection(wing_reader.GetOutputPort())

wing_actor = vtkActor()
wing_actor.SetMapper(wing_mapper)

renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(arrow_actor)
renderer.AddActor(wing_actor)
colors = vtkNamedColors()
renderer.SetBackground(colors.GetColor3d("Gray"))  # type: ignore

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.Start()
