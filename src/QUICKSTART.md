# Lathe - Quick Start Guide

Get up and running with the new Lathe architecture in 5 minutes.

## Prerequisites

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install PostgreSQL with PostGIS (optional but recommended)
# On Ubuntu/Debian:
sudo apt install postgresql postgis

# On macOS:
brew install postgresql postgis
```

## Installation

```bash
# Clone repository
git clone https://github.com/NorthernScott/lathe.git
cd lathe

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

## Quick Test - Generate Your First World

```bash
# Create data directory
mkdir -p data/worlds

# Run the basic example
cd src_new
python examples/basic_generation.py
```

This will:
1. Generate a world with terrain and tectonic plates
2. Detect points of interest
3. Save to HDF5 format
4. Display statistics

Expected output:
```
Generating world: Example World
  Recursion: 5 (6378100 m radius)
  Seed: 42

[10:30:15] plugin_started: Starting plugin: terrain
terrain      [██████████████████████████████████] 100.0%
✓ Completed: terrain

[10:30:18] plugin_started: Starting plugin: tectonics
tectonics    [██████████████████████████████████] 100.0%
✓ Completed: tectonics

World generation complete!
  Mesh points: 10,242
  Mesh faces: 20,480
  ...
```

## Complete Workflow Example

For a more comprehensive example with progress bars and detailed statistics:

```bash
python examples/complete_workflow.py
```

This demonstrates:
- Full generation pipeline
- POI detection and analysis
- Data storage and loading
- Export to VTK format
- Statistics and summaries

## Using the API Server

### Start the server

```bash
python -m lathe.api.server
```

Server starts at `http://localhost:8000`

### API Documentation

Open in browser: `http://localhost:8000/docs`

Interactive Swagger UI for testing all endpoints.

### Generate a world via API

```bash
# Using curl
curl -X POST "http://localhost:8000/worlds/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API World",
    "recursion": 5,
    "seed": 999,
    "pipeline": ["terrain", "tectonics"]
  }'

# Using Python requests
import requests

response = requests.post("http://localhost:8000/worlds/generate", json={
    "name": "API World",
    "recursion": 5,
    "seed": 999,
    "pipeline": ["terrain", "tectonics"]
})

print(response.json())
```

### List worlds

```bash
curl "http://localhost:8000/worlds"
```

### Analyze POIs

```bash
curl -X POST "http://localhost:8000/worlds/{world_id}/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "detect_mountains": true,
    "detect_settlements": true,
    "min_importance": 0.7
  }'
```

## Python API Usage

### Basic Generation

```python
import asyncio
from lathe.core.engine import WorldGenerationEngine
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin

async def main():
    # Create and configure engine
    engine = WorldGenerationEngine()
    engine.register_plugin(TerrainGeneratorPlugin())

    # Generate world
    world = await engine.generate_world(
        params=WorldParameters(name="Test", recursion=5),
        pipeline=["terrain"],
    )

    print(f"Generated: {world.params.name}")
    print(f"Points: {world.num_points:,}")

asyncio.run(main())
```

### With Progress Tracking

```python
from lathe.core.events import get_global_emitter, EventType

def on_progress(event):
    progress = event.data.get("progress", 0)
    print(f"{event.data['plugin']}: {progress:.1%}")

emitter = get_global_emitter()
emitter.subscribe(EventType.PLUGIN_PROGRESS, on_progress)

# Now run generation...
```

### Saving and Loading

```python
from lathe.storage.mesh_store import MeshStore

store = MeshStore("./data/worlds")

# Save
path = store.save_world(world, compress=True)

# Load
loaded = store.load_world(world.id)

# List all
worlds = store.list_worlds()
for w in worlds:
    print(f"{w['name']}: {w['num_points']:,} points")
```

## Configuration

### Database Setup (Optional)

If using PostgreSQL for metadata storage:

```bash
# Create database
createdb lathe

# Enable PostGIS extension
psql -d lathe -c "CREATE EXTENSION postgis;"

# Update connection string in code
metadata_store = MetadataStore(
    database_url="postgresql://username:password@localhost/lathe"
)
```

### Environment Variables

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql://localhost/lathe

# Storage
HDF5_STORAGE_DIR=./data/worlds

# API
API_HOST=0.0.0.0
API_PORT=8000

# Generation
DEFAULT_RECURSION=6
DEFAULT_WORKERS=4
```

## Directory Structure After First Run

```
lathe/
├── src_new/              # New architecture code
│   ├── lathe/
│   └── examples/
├── data/                 # Generated data (created on first run)
│   └── worlds/           # Saved worlds (HDF5 files)
│       ├── world_<uuid>.h5
│       └── world_<uuid>.vtk
├── .venv/                # Virtual environment
└── pyproject.toml
```

## Common Commands

```bash
# Generate world
python examples/basic_generation.py

# Run complete workflow
python examples/complete_workflow.py

# Start API server
python -m lathe.api.server

# Run tests
pytest

# Type checking
pyright

# Code formatting
ruff format .

# Linting
ruff check .
```

## Troubleshooting

### Import errors
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall dependencies
uv sync
```

### PostgreSQL connection errors
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Create database if missing
createdb lathe

# Update connection string in code
```

### HDF5 errors
```bash
# Reinstall h5py
uv pip install --force-reinstall h5py
```

## Visualization

### Desktop Viewer

Launch the interactive 3D viewer:

```bash
# From src_new directory
python -m lathe.viz.desktop

# Or with specific world ID
python -m lathe.viz.desktop <world_id>
```

Features:
- Interactive 3D globe
- Data layer switching
- World selector
- Information panel
- RGB coordinate axes

### Export to ParaView

```bash
# VTK files are created by examples
paraview data/worlds/world_*.vtk
```

### Off-Screen Rendering

```python
import pyvista as pv
from lathe.storage.mesh_store import MeshStore

store = MeshStore("./data/worlds")
world = store.load_world(world_id)

plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(world.mesh, scalars="elevation", cmap="terrain")
plotter.screenshot("world.png")
```

## Testing

Run comprehensive tests:

```bash
# Test all visualization and export
python test_all_visualization.py

# Test viewer components
python test_viewer.py
```

## Next Steps

1. **Read the full README**: `src_new/README.md`
2. **Explore examples**: `src_new/examples/`
3. **Test Report**: `src_new/TEST_REPORT.md` - See all test results
4. **API documentation**: `http://localhost:8000/docs` (when server running)
5. **Create custom plugins**: See `PLUGIN_DEVELOPMENT_GUIDE.md`
6. **Launch desktop viewer**: `python -m lathe.viz.desktop`

## Getting Help

- **Documentation**: See `src_new/README.md`
- **Examples**: See `src_new/examples/`
- **Issues**: https://github.com/NorthernScott/lathe/issues
- **API Docs**: http://localhost:8000/docs

## Key Concepts

### Plugin System
Simulations are modular plugins that can be composed in pipelines:
- **Terrain** → generates base elevation
- **Tectonics** → adds plate boundaries (requires terrain)
- **Erosion** → simulates weathering (requires terrain)
- **Climate** → models temperature/precipitation

### Data Layers
World mesh stores multiple data layers:
- `elevation` - terrain height
- `plate_id` - tectonic plate assignment
- `temperature` - climate data
- `precipitation` - rainfall
- (custom layers from your plugins)

### Async Execution
Engine runs plugins asynchronously:
- Independent plugins run in parallel
- Dependencies are auto-resolved
- Progress reported via events
- Non-blocking UI

### Storage
Two-tier storage system:
- **HDF5** - efficient mesh data storage
- **PostgreSQL** - queryable metadata and POIs

Enjoy building worlds with Lathe! 🌍
