# Lathe - New Architecture

This is the redesigned architecture for Lathe, a 3D procedural world generation engine for creating spherical worlds for tabletop RPGs and world-building.

## Architecture Overview

The new architecture is a **modular monolith with plugin system**:

```
┌─────────────────────────────────────────┐
│          Frontend Layer                 │
│  (PyVista/Qt Desktop or Web)           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         FastAPI REST API                │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     World Generation Engine             │
│  - Plugin orchestration                 │
│  - Async execution                      │
│  - Event system                         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Simulation Plugins                 │
│  • Terrain   • Tectonics                │
│  • Erosion   • Hydrology                │
│  • Climate   • Insolation               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Storage Layer                   │
│  HDF5 (mesh) + PostgreSQL (metadata)   │
└─────────────────────────────────────────┘
```

## Key Features

### Plugin System
- **Modular simulations**: Each simulation (terrain, tectonics, climate) is a standalone plugin
- **Dependency management**: Automatic resolution of plugin dependencies
- **Parallel execution**: Independent plugins run concurrently
- **Progress reporting**: Real-time event system for progress updates

### Data Storage
- **HDF5 for mesh data**: Efficient storage of large numerical arrays with compression
- **PostgreSQL + PostGIS for metadata**: POIs, spatial queries, world metadata
- **Hybrid approach**: Best tool for each job

### Async Architecture
- **Non-blocking**: UI remains responsive during long computations
- **ThreadPoolExecutor**: CPU-intensive work runs in background
- **Event-driven**: Progress updates via event system

### REST API
- **FastAPI**: Modern async Python framework
- **WebSocket support**: Real-time progress updates
- **Auto-documented**: OpenAPI/Swagger docs

## Directory Structure

```
src_new/lathe/
├── core/               # Core engine and orchestration
│   ├── engine.py       # WorldGenerationEngine
│   └── events.py       # Event system
│
├── models/             # Data models
│   └── world.py        # World class
│
├── plugins/            # Simulation plugins
│   ├── base.py         # Plugin interfaces
│   ├── terrain/        # Terrain generation
│   ├── tectonics/      # Plate tectonics
│   ├── erosion/        # Erosion simulation (TODO)
│   ├── hydrology/      # Water and rivers (TODO)
│   ├── climate/        # Climate modeling (TODO)
│   └── insolation/     # Solar radiation (TODO)
│
├── analysis/           # Analysis plugins
│   └── poi_detector.py # Point of Interest detection
│
├── storage/            # Data persistence
│   ├── mesh_store.py   # HDF5 storage
│   └── metadata_store.py # PostgreSQL storage
│
├── api/                # REST API
│   └── server.py       # FastAPI server
│
└── viz/                # Visualization (TODO)
    ├── desktop.py      # PyVista/Qt viewer
    └── web.py          # Web-based viewer
```

## Getting Started

### Prerequisites

1. **Python 3.10+** (3.13 recommended)
2. **PostgreSQL with PostGIS** (optional, for metadata storage)
3. **UV** (Python package manager)

### Installation

```bash
# Install dependencies
uv sync

# Optional: Set up PostgreSQL database
createdb lathe
psql -d lathe -c "CREATE EXTENSION postgis;"
```

### Basic Usage

```python
import asyncio
from lathe.core.engine import WorldGenerationEngine
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin

async def main():
    # Create engine
    engine = WorldGenerationEngine()

    # Register plugins
    engine.register_plugin(TerrainGeneratorPlugin())
    engine.register_plugin(TectonicsSimulatorPlugin())

    # Define parameters
    params = WorldParameters(
        name="My World",
        recursion=6,
        seed=42,
    )

    # Generate world
    world = await engine.generate_world(
        params=params,
        pipeline=["terrain", "tectonics"],
    )

    print(f"Generated: {world.params.name}")
    print(f"Points: {world.num_points:,}")

asyncio.run(main())
```

See `examples/` for more detailed usage examples.

### Running the API Server

```bash
# Start the FastAPI server
python -m lathe.api.server

# Or with uvicorn directly
uvicorn lathe.api.server:app --reload

# API docs at: http://localhost:8000/docs
```

## Creating a Plugin

### Simulation Plugin

```python
from lathe.plugins.base import SimulationPlugin, PluginMetadata, PluginResult

class MySimulationPlugin(SimulationPlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_simulation",
            version="1.0.0",
            dependencies=["terrain"],  # Requires terrain first
            description="My custom simulation",
        )

    def get_required_data_layers(self) -> list[str]:
        return ["elevation"]  # Needs elevation data

    def get_produced_data_layers(self) -> list[str]:
        return ["my_data"]  # Produces my_data layer

    async def execute(self, world, params, progress_callback):
        # Your simulation logic here
        # Update world.add_data_layer("my_data", data)

        if progress_callback:
            progress_callback(0.5, "Halfway done")

        return PluginResult(success=True, message="Complete")
```

### Analysis Plugin

```python
from lathe.plugins.base import AnalysisPlugin, PluginMetadata, PluginResult

class MyAnalysisPlugin(AnalysisPlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_analyzer",
            version="1.0.0",
            description="Analyzes world features",
        )

    async def analyze(self, world, params, progress_callback):
        # Analyze the world
        results = {"feature_count": 42}

        return PluginResult(
            success=True,
            message="Analysis complete",
            data=results,
        )
```

## Storage

### Saving and Loading Worlds

```python
from lathe.storage.mesh_store import MeshStore

# Create store
store = MeshStore(storage_dir="./data/worlds")

# Save world
path = store.save_world(world, compress=True)

# Load world
loaded_world = store.load_world(world.id)

# List all worlds
worlds = store.list_worlds()

# Export to VTK
store.export_to_vtk(world.id, "output.vtk")
```

### PostgreSQL Metadata

```python
from lathe.storage.metadata_store import MetadataStore

# Create store
meta_store = MetadataStore(
    database_url="postgresql://user:password@localhost/lathe"
)

# Create tables
meta_store.create_tables()

# Save world metadata
meta_store.save_world_metadata(
    world_id=world.id,
    name=world.params.name,
    hdf5_path=str(hdf5_path),
    parameters=world.params.__dict__,
    metadata=world.metadata,
)

# Add POI
meta_store.add_poi(
    world_id=world.id,
    poi_id=uuid4(),
    poi_type="mountain",
    location=(x, y, z),
    mesh_point_index=1234,
    name="Mount Example",
    properties={"elevation": 5000},
    importance=0.9,
)

# Query POIs
pois = meta_store.get_pois(world.id, poi_type="mountain")
```

## API Endpoints

### Generate World
```bash
POST /worlds/generate
{
  "name": "My World",
  "recursion": 6,
  "pipeline": ["terrain", "tectonics"]
}
```

### List Worlds
```bash
GET /worlds
```

### Get World Info
```bash
GET /worlds/{world_id}
```

### Analyze POIs
```bash
POST /worlds/{world_id}/analyze
{
  "detect_mountains": true,
  "detect_settlements": true,
  "min_importance": 0.7
}
```

### Get POIs
```bash
GET /worlds/{world_id}/pois?poi_type=mountain&min_importance=0.5
```

### WebSocket Progress
```bash
WS /ws/worlds/{world_id}
```

## Event System

Subscribe to events for progress tracking:

```python
from lathe.core.events import get_global_emitter, EventType

emitter = get_global_emitter()

def on_progress(event):
    print(f"{event.message} - {event.data.get('progress', 0):.1%}")

emitter.subscribe(EventType.PLUGIN_PROGRESS, on_progress)
```

## Testing

```bash
# Run tests
pytest

# Run type checking
pyright

# Run linting
ruff check .

# Format code
ruff format .
```

## Migration from Old Architecture

The old architecture (in `src/lathe/`) remains functional. To migrate:

1. **Plugins**: Refactor simulation code into plugin classes
2. **World class**: Update to use new `World` model
3. **Storage**: Convert to HDF5/PostgreSQL
4. **Visualization**: Update to work with new data layers

See migration guide in `docs/migration.md` (TODO).

## Future Development

### Planned Plugins
- [ ] Erosion simulation (hydraulic + thermal)
- [ ] Hydrology (rivers, lakes, watersheds)
- [ ] Climate modeling (temperature, precipitation, wind)
- [ ] Insolation calculator (solar radiation)
- [ ] Biomes (based on climate + terrain)
- [ ] Resources (minerals, forests, etc.)

### Frontend Development
- [ ] Enhanced PyVista/Qt desktop viewer
- [ ] Web-based 3D viewer (Three.js)
- [ ] Wiki-style POI explorer
- [ ] Layer switching UI
- [ ] Real-time generation monitoring

### Performance
- [ ] GPU acceleration for simulations
- [ ] Multi-machine distributed generation
- [ ] Incremental mesh refinement
- [ ] Level-of-detail rendering

## Contributing

See `CONTRIBUTING.md` for development guidelines.

## License

MIT License - see `LICENSE` file.

## Acknowledgments

- Inspired by [Azgaar's Fantasy Map Generator](https://azgaar.github.io/Fantasy-Map-Generator/)
- Built with [PyVista](https://pyvista.org/), [FastAPI](https://fastapi.tiangolo.com/), and [HDF5](https://www.hdfgroup.org/)
