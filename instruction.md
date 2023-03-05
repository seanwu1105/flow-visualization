# Assignment 4: Flow Visualization

## Objective

The topic of this assignment is flow visualization. You will study a delta wing
dataset and visualize the velocity information using vector field visualization
techniques. Your task will be to show the major flow structures present in the
dataset (primary and secondary vortices and a recirculation bubble on each side
of the wing). In addition, you will visualize the spatial relationship that
exists between the velocity (vector) field and the pressure (scalar) field.
Refer to the corresponding instructions below.

## Task 1: Glyphs

Your first task consists in using cutting planes to probe the vector values.
Specifically, you will create a plane orthogonal to the X-axis of the volume
(the main axis of the wing) and sample the velocity vector field on that plane.
You will need to follow an approach similar to what is demonstrated in
[ProbeCombustor.py](https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/ProbeCombustor/)
for that purpose. To represent individual vectors as arrows, you will use
[vtkArrowSource](https://vtk.org/doc/nightly/html/classvtkArrowSource.html) as
the source of a
[vtkGlyph3D](https://vtk.org/doc/nightly/html/classvtkGlyph3D.html) filter. Use
3 planes at 3 different locations along the X axis (with normal pointing along
the X direction) to capture the structures mentioned above. Show the delta wing
geometry in each image for context (the corresponding geometry is provided as
[vtkPolyData](https://vtk.org/doc/nightly/html/classvtkPolyData.html) in a
separate file).

Deliverables: Create an executable named `three_planes.py` that contains the
(hardcoded) information needed to visualize the vector glyphs on the 3 planes
that you have selected. Your executable should receive the names of two files
from the command line, namely the CFD file containing the vector field
information and the file containing the geometry of the delta wing.

```sh
python three_planes.py <vfem.vtu> <wing.vtp>
```

Report: Explain in the report how you selected the planes used in your
implementation and comment on the properties of the flow that you can discern in
your visualization. Include pictures showing each cutting plane individually
(along with the associated glyphs) as well as other images showing all planes
and the wing together.

## Task 2: Streamlines, Stream Tubes, and Stream Surfaces

Task 1 should provide you with a general sense of the location of interesting
structures in the flow volume. Your second task now consists in using
streamlines, stream tubes, and stream surfaces, as demonstrated in
[officeTubes.py](https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/OfficeTube/)
and
[streamSurface.py](https://vtk.org/doc/nightly/html/classvtkStreamSurface.html)
to show how the flow swirls around the vortices present in the data.

Deliverables: You will construct 3 visualizations for this task.

- A first executable showing a large number (between 50 and 200) of streamlines.
- A second executable showing a small number of stream tubes
- A third executable showing a stream surface seeded along an appropriately
  chosen line segment (aka rake).

In each case, the seeding locations and the other parameters of the technique
must be hardcoded in your program. You must choose parameter values that produce
good-quality results and capture the behavior of the flow around the vortices on
each side of the wing. Note that each visualization should represent the
velocity magnitude using color coding, and the corresponding color scale should
be provided for reference. Show the delta wing geometry in each image for
context.

```sh
streamlines <vfem.vtu> <wing.vtp>
streamtubes <vfem.vtu> <wing.vtp>
streamsurfaces <vfem.vtu> <wing.vtp>
```

Report: Explain in the report how the seeding locations were chosen for each of
these three techniques and how they relate to the observations made in Task 1.

## Task 3: Combining Scalar and Vector Visualization

The scalar and vector information available for this dataset provides two
complementary perspectives on the properties of the flow. For the third task of
this assignment, you will combine isosurfaces of pressure (available as a scalar
attribute in vfem.vtu) with streamlines to visualize the relationship between
the streamlines’ geometry and the shape of the isosurfaces. Create
visualizations in which the streamline seeds and the isovalues of the isosurface
are chosen in such a way as to best illustrate the correlation between the two
kinds of objects. Hint: Vortices, especially their core region, correspond to
regions of low pressure.

Deliverables: Create an executable named combined.py that produces a
visualization of the CFD dataset, combining isosurfaces of the pressure,
streamlines of the velocity vector field, and geometry of the delta wing. The
various parameters needed to create the visualization must be hardcoded in the
program. As in the previous tasks, your executable should receive from the
command line the names of the three files needed to create the visualization:
velocity (+pressure) dataset and wing geometry description.

```sh
python combined.py <vfem.vtu> <wing.vtp>
```

Report: Describe in the report the things you tried before arriving at the
proposed solution and explain why your final selection is a good one. Show the
delta wing geometry in each image for context.

## Task 4: Analysis

Considering your results in Task 1 and Task 2 of the assignment, comment on the
effectiveness of the resulting visualizations for your understanding of this
dataset. What were the pros and cons of each technique? Comment on the results
you were able to achieve in Task 3 by integrating isosurfacing and vector
visualization. Did you find this combination beneficial? Provide a justified
answer to each of these questions in the report.

## Data Sets

The CFD dataset used in this project is available as a (fairly) large
[vtkUnstructuredGrid](https://vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html).
The information available corresponds to the velocity (vector field) and the
pressure (scalar field). A separate file describing the geometry of the delta
wing is also available (a vtkPolyData). Note that the CFD simulation that
produced this dataset used adaptive mesh refinement, which explains the vast
discrepancies that exist between the resolution of the mesh next to the wing and
further away from it.

Get the data from
[here](https://www.cs.purdue.edu/homes/cs530/projects/project4.html).
