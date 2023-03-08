from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader

VELOCITY_ARRAY_NAME = "velocity"


def read_vfem_velocity(vfem_filename: str):
    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(vfem_filename)
    reader.Update()
    velocity_range: tuple[float, float] = (
        reader.GetOutput().GetPointData().GetArray(VELOCITY_ARRAY_NAME).GetRange()
    )

    return reader, velocity_range
