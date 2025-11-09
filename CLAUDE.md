# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lathe of Heaven is a procedural world generation tool for creating spherical worlds for tabletop RPGs. It generates realistic planetary features including elevations, tectonic plates, and terrain using noise generation and physics simulation.

## Development Commands

### Environment Setup

This repo uses UV to manage Python versions, packages, and builds.

```bash
# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
uv sync
```

### Running the Application

```bash
# Run the main application (creates a world with visualization)
python -m lathe

# Or run directly from source
python src/lathe/__main__.py
```

### Code Quality
```bash
# Format code with Ruff
ruff format .

# Lint code with Ruff
ruff check .

# Fix auto-fixable linting issues
ruff check --fix .

# Type checking with Pyright
pyright

# Run tests with pytest
pytest
```

### Docker Development
```bash
# Build and start development environment
docker compose -f ".docker/dev-compose.yml" -p lathe up -d --build

# Attach to container
docker attach lathe-app

# Run inside container
poetry run python3 lathe/lathe.py --help
```

Note: Create `.docker/app_user_password.txt` (UTF-8, plaintext password) before Docker build.

## Architecture

### Core Components

**World Generation Pipeline** (`src/lathe/engine/world.py`)
- `World` class is the central component that manages all world data
- Uses PyVista's `Icosphere` to create a subdivided spherical mesh
- World parameters: radius, recursion level (mesh detail), seed, ocean_percent, elevation ranges
- Key methods:
  - `generate_elevations()`: Creates terrain using OpenSimplex noise with multiple octaves
  - `create_tectonic_plates()`: Assigns mesh points to tectonic plates using KDTree nearest-neighbor
  - Elevations are applied as point data on the mesh and warped by scalar values

**Noise-Based Terrain** (`src/lathe/engine/world.py:133-197`)
- Uses OpenSimplex 4D noise for continuous, smooth elevation generation
- Multiple octaves with roughness (frequency) and persistence (amplitude) controls
- Elevations are normalized, rescaled to zmin/zmax range, then warped by zscale factor
- Landforms determined by elevation >= 0 threshold

**Tectonic Simulation** (`src/lathe/engine/tectonics.py`)
- Older implementation using 2D arrays and scipy for plate detection
- `generate_plates()`: Finds local maxima as plate centers
- `simulate_tectonics()`: Moves plates and handles collisions to modify elevations
- Note: Currently world.py uses a different approach with KDTree for 3D spherical plates

**Visualization** (`src/lathe/engine/viz.py`)
- `Visualizer` class renders worlds using PyVista 3D plotting
- Dark theme with cmocean colormaps (specifically `cmo.topo` for elevation)
- Interactive scalar selection via checkbox widget to switch between datasets (elevations, tectonic plates, etc.)
- Mesh data stored as point_data on the PyVista mesh object

**GUI** (`src/lathe/gui/`)
- PySide6/Qt-based GUI (QML interface in main.qml)
- Currently basic implementation that creates test world and visualizer

### Data Flow
1. Initialize `World` with parameters (radius, recursion, seed, etc.)
2. Call `generate_elevations()` to create base terrain using noise
3. Call `create_tectonic_plates()` to partition world into plates
4. Pass `World` to `Visualizer` to render 3D visualization
5. User can toggle between different scalar datasets (elevations, plates, etc.)

### Key Technologies
- **PyVista**: 3D mesh creation, manipulation, and visualization
- **OpenSimplex**: Procedural noise generation
- **NumPy**: Array operations and numerical computing
- **SciPy**: Spatial algorithms (KDTree) and signal processing
- **PySide6**: Qt GUI framework
- **cmocean**: Scientific colormaps for oceanography

## Code Style

- Line length: 120 characters (Ruff and Pyright configured)
- Python version: 3.13 (target), minimum 3.10
- Use double quotes for strings
- Type hints required (enforced by Pyright)
- Ruff ignores: D100 (module docstrings), S311 (non-crypto random), FIX002/FIX004 (TODO/HACK comments), TD003 (todo links)

## Important Patterns

**Mesh Point Data Storage**
All generated data (elevations, plates, landforms) is stored as point_data on the PyVista mesh:
```python
self.mesh.point_data["Elevations"] = rescaled_elevations
self.mesh.point_data["Tectonic Plates"] = self.plate_indices
```

**Scalar Warping**
Mesh geometry is modified by warping points along normals using scalar values:
```python
self.mesh.warp_by_scalar(scalars="Elevations", factor=self.zscale, inplace=True)
```

**Random Name Generation**
Worlds are given random names from `planetnames.json` at repo root if not specified.
