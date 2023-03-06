from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)


def build_window(actors: list[vtkActor], actors_2d: list[vtkActor2D]):
    renderer = vtkRenderer()
    for actor in actors:
        renderer.AddActor(actor)
    for actor_2d in actors_2d:
        renderer.AddActor2D(actor_2d)
    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("Gray"))  # type: ignore

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(640, 480)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    return interactor
