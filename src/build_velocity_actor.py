from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from src.read_vfem_velocity import VELOCITY_ARRAY_NAME


def build_velocity_actor(
    output_port: vtkAlgorithmOutput, velocity_range: tuple[float, float]
):
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(output_port)
    mapper.GetLookupTable().SetVectorModeToMagnitude()
    mapper.SetScalarModeToUsePointFieldData()
    mapper.SelectColorArray(VELOCITY_ARRAY_NAME)
    mapper.SetScalarRange(velocity_range)

    actor = vtkActor()
    actor.SetMapper(mapper)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(mapper.GetLookupTable())  # type: ignore

    return actor, scalar_bar
