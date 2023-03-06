from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)


def build_window(
    actors: list[vtkActor], actors_2d: list[vtkActor2D], depth_peeling: bool = False
):
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

    if depth_peeling:
        render_window.SetAlphaBitPlanes(True)
        render_window.SetMultiSamples(0)
        renderer.SetUseDepthPeeling(True)
        renderer.SetMaximumNumberOfPeels(100)
        renderer.SetOcclusionRatio(0.0)

    return interactor
