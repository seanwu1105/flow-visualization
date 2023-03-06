from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.build_window import build_window
from src.build_wing_actor import build_wing_actor
from src.parse_args import parse_args
from src.vtk_side_effects import import_for_rendering_core

import_for_rendering_core()
args = parse_args()


wing_filename = args.wing
vfem_filename = args.vfem

seeds = vtkPlaneSource()
seeds.SetResolution(15, 15)
seeds.SetNormal(1, 0, 0)

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(vfem_filename)

streamline = vtkStreamTracer()
streamline.SetSourceConnection(seeds.GetOutputPort())
streamline.SetInputConnection(reader.GetOutputPort())

streamline_mapper = vtkDataSetMapper()
streamline_mapper.SetInputConnection(streamline.GetOutputPort())
streamline_mapper.ScalarVisibilityOff()

streamline_actor = vtkActor()
streamline_actor.SetMapper(streamline_mapper)

contour_range = [40900.0, 43721.0]

contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.GenerateValues(8, contour_range)

contour_mapper = vtkDataSetMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(contour_range)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetOpacity(0.1)

build_window(
    [build_wing_actor(wing_filename), streamline_actor, contour_actor],
    [],
    depth_peeling=True,
).Start()
