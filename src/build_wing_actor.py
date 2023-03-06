from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper


def build_wing_actor(filename: str):
    reader = vtkXMLPolyDataReader()
    reader.SetFileName(filename)

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor
