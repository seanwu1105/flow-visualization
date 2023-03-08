# Flow Visualization

CS530 Introduction to Scientific Visualization assignment 4 @Purdue.

## Dataset

See [instruction](./instruction.md).

## Getting Started

Install Python 3.10 or later.

Install Poetry **1.3.2 or later**. See
[Poetry's documentation](https://python-poetry.org/docs/) for details.

> Poetry earlier than 1.3 will not work.

Install the project's dependencies:

```sh
poetry install --no-root
```

Activate the virtual environment:

```sh
poetry shell
```

Execute the applications with the following commands for different visualization
tasks:

```sh
python three_planes.py <vfem.vtu> <wing.vtp>
python streamlines.py <vfem.vtu> <wing.vtp>
python streamtubes.py <vfem.vtu> <wing.vtp>
python stteamsurfaces.py <vfem.vtu> <wing.vtp>
python combined.py <vfem.vtu> <wing.vtp>
```

You can find the datasets in the `assets` directory.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
