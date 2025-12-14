# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lathe of Heaven is a 3D procedural world generation engine for creating spherical worlds for tabletop RPGs. It uses a modular plugin-based architecture with async execution, event-driven progress reporting, and hybrid HDF5/PostgreSQL storage.

## Key Commands

### Environment Setup
```bash
# Install dependencies (requires UV package manager)
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Development
```bash
# Run type checking
pyright

# Lint code
ruff check .

# Format code
ruff format .

# Run all tests
pytest

# Run specific test file
pytest src/tests/unit/test_engine.py

# Run tests with coverage
pytest --cov=lathe --cov-report=html
```

### Running the Application
```bash
# Launch desktop 3D viewer
python -m lathe.viz.desktop

# Launch desktop viewer with specific world ID
python -m lathe.viz.desktop <world_id>

# Start FastAPI server
python -m lathe.api.server
# or
uvicorn lathe.api.server:app --reload

# Run basic world generation example
cd src
python examples/basic_generation.py

# Run complete workflow example
python examples/complete_workflow.py
```

### Entry Points
```bash
# Main entry point (defined in pyproject.toml)
lathe

# Available as Python module
python -m lathe
```

## Architecture

### Plugin System
The core architecture is a **modular plugin-based engine** with dependency resolution and parallel execution:

- **Plugins are registered with the engine** via `engine.register_plugin(plugin)`
- **Dependencies are auto-resolved** using NetworkX dependency graphs
- **Parallel execution** occurs when plugins have no dependencies on each other
- **Event-driven progress** reporting via global event emitter
- **Thread pool** for CPU-intensive work to keep async loop responsive

#### Plugin Types
1. **SimulationPlugin**: Modifies the world by adding/updating data layers
   - Example: TerrainGeneratorPlugin, TectonicsSimulatorPlugin
   - Must declare required and produced data layers
   - Executed in dependency order

2. **AnalysisPlugin**: Examines world without modifying it
   - Example: POIDetectorPlugin
   - Used for POI detection, resource mapping, habitability analysis

#### Creating a New Plugin
All plugins must:
- Inherit from `SimulationPlugin` or `AnalysisPlugin` in `lathe.plugins.base`
- Implement `metadata` property returning `PluginMetadata`
- Implement `execute()` or `analyze()` async method
- Declare data layer requirements via `get_required_data_layers()`
- Declare produced layers via `get_produced_data_layers()`
- Use `asyncio.get_event_loop().run_in_executor()` for CPU-intensive work
- Report progress via optional `progress_callback(progress: float, message: str)`

See `src/PLUGIN_DEVELOPMENT_GUIDE.md` for detailed plugin development instructions.

### World Generation Pipeline
Execution flow:
1. Create `WorldGenerationEngine()`
2. Register plugins: `engine.register_plugin(plugin)`
3. Call `await engine.generate_world(params, pipeline, plugin_params)`
4. Engine:
   - Creates World object with icosphere mesh
   - Validates plugin dependencies
   - Orders plugins using topological sort
   - Executes plugins in parallel where possible
   - Reports progress via event system

### Data Model
- **World**: Central data structure containing icosphere mesh + data layers
  - Mesh: PyVista PolyData (icosphere geometry)
  - Data layers: Named numpy arrays (elevation, plate_id, temperature, etc.)
  - Methods: `add_data_layer()`, `get_data_layer()`, `has_data_layer()`, `list_data_layers()`

- **WorldParameters**: Configuration for world generation
  - `recursion`: Mesh subdivision level (5-7 typical, higher = more points)
  - `radius`: Planet radius in meters (default: Earth ~6.378M)
  - `seed`: Random seed for reproducibility

### Storage Architecture
**Hybrid storage approach:**

1. **HDF5 (MeshStore)** - Efficient storage of large mesh data
   - Location: `data/worlds/world_<uuid>.h5`
   - Stores: mesh geometry, all data layers, world metadata
   - Features: Compression, fast array access, VTK export
   - Usage: `MeshStore(storage_dir).save_world(world)`

2. **PostgreSQL + PostGIS (MetadataStore)** - Queryable metadata
   - Stores: World metadata, POIs with spatial queries
   - Optional but recommended for POI features
   - Usage: `MetadataStore(database_url).save_world_metadata()`

### Event System
Global event emitter for progress tracking:
```python
from lathe.core.events import get_global_emitter, EventType

emitter = get_global_emitter()
emitter.subscribe(EventType.PLUGIN_PROGRESS, callback)
emitter.emit(EventType.PLUGIN_PROGRESS, message, data)
```

Event types:
- `PLUGIN_STARTED`, `PLUGIN_PROGRESS`, `PLUGIN_COMPLETED`, `PLUGIN_FAILED`
- `WORLD_GENERATION_STARTED`, `WORLD_GENERATION_COMPLETED`
- `ANALYSIS_STARTED`, `ANALYSIS_COMPLETED`

### Directory Structure
```
lathe/
├── src/lathe/              # Main source code
│   ├── core/               # Core engine and events
│   │   ├── engine.py       # WorldGenerationEngine
│   │   └── events.py       # Event system
│   ├── models/             # Data models
│   │   └── world.py        # World class
│   ├── plugins/            # Simulation plugins
│   │   ├── base.py         # Plugin base classes
│   │   ├── terrain/        # Terrain generation
│   │   ├── tectonics/      # Plate tectonics
│   │   ├── erosion/        # TODO
│   │   ├── hydrology/      # TODO
│   │   ├── climate/        # TODO
│   │   └── insolation/     # TODO
│   ├── analysis/           # Analysis plugins
│   │   └── poi_detector.py # POI detection
│   ├── storage/            # Storage layer
│   │   ├── mesh_store.py   # HDF5 storage
│   │   └── metadata_store.py # PostgreSQL
│   ├── api/                # FastAPI REST API
│   │   └── server.py       # API endpoints
│   └── viz/                # Visualization
│       ├── desktop.py      # PyVista/Qt viewer
│       └── __main__.py     # Entry point for viz
├── src/tests/              # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── conftest.py         # Pytest fixtures
├── src/examples/           # Example scripts
├── data/worlds/            # Generated world data (gitignored)
└── pyproject.toml          # Project configuration
```

## Technology Stack

- **Python 3.13** (strict requirement)
- **UV** for package management
- **PyVista** for 3D mesh visualization
- **PySide6** for Qt-based desktop UI
- **NumPy/SciPy** for numerical computations
- **NetworkX** for dependency graph resolution
- **HDF5** (h5py) for mesh data storage
- **FastAPI** for REST API (TODO)
- **PostgreSQL + PostGIS** for metadata (optional)
- **OpenSimplex** for noise generation

## Important Patterns

### Async Pattern for CPU-Intensive Work
All plugin execution uses this pattern:
```python
async def execute(self, world, params, progress_callback):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,  # Uses engine's ThreadPoolExecutor
        self._sync_method,
        world,
        params,
        progress_callback,
    )
```

### Data Layer Validation
Plugins declare dependencies and engine validates before execution:
```python
def get_required_data_layers(self) -> list[str]:
    return ["elevation"]  # Must exist before plugin runs

def get_produced_data_layers(self) -> list[str]:
    return ["plate_id"]  # Will be created by plugin
```

### Progress Reporting
Always report progress for long operations:
```python
if progress_callback:
    progress_callback(0.5, "Halfway through simulation")
```

### Error Handling in Plugins
Return PluginResult for structured error handling:
```python
try:
    # ... plugin logic ...
    return PluginResult(success=True, message="Complete", data=stats)
except Exception as e:
    return PluginResult(success=False, message=f"Failed: {e}")
```

## Testing

### Test Organization
- `src/tests/unit/` - Unit tests for individual components
- `src/tests/integration/` - Integration tests for full workflows
- `src/tests/conftest.py` - Shared pytest fixtures
- `src/tests/fixtures/` - Test data fixtures

### Running Tests
Tests use pytest with async support (`pytest-asyncio`). All async tests must be marked with `@pytest.mark.asyncio`.

## GitHub Actions

The repository has automated Claude Code review configured:
- Workflow: `.github/workflows/claude-code-review.yml`
- Triggers: On PR open/sync
- Uses: `anthropics/claude-code-action@v1`
- Posts review comments directly to PRs using `gh pr comment`

**Important**: When modifying GitHub Actions workflows, avoid nested quotes in YAML. Use unquoted values for `--allowed-tools` arguments:
```yaml
# Correct:
claude_args: --allowed-tools Bash(gh pr view:*),Bash(gh pr comment:*)

# Incorrect (causes parsing errors):
claude_args: '--allowed-tools "Bash(gh pr view:*),Bash(gh pr comment:*)"'
```

## Common Workflows

### Generate a World
```python
import asyncio
from lathe.core.engine import WorldGenerationEngine
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin

engine = WorldGenerationEngine()
engine.register_plugin(TerrainGeneratorPlugin())
engine.register_plugin(TectonicsSimulatorPlugin())

world = await engine.generate_world(
    params=WorldParameters(name="My World", recursion=6, seed=42),
    pipeline=["terrain", "tectonics"],
)
```

### Save and Load Worlds
```python
from lathe.storage.mesh_store import MeshStore

store = MeshStore("./data/worlds")
path = store.save_world(world, compress=True)
loaded_world = store.load_world(world.id)
```

### Launch Interactive Viewer
```python
from lathe.viz.desktop import launch_viewer

# From command line:
python -m lathe.viz.desktop [world_id]
```

## Performance Considerations

- **Mesh recursion levels**: Each level ~4x more points
  - recursion=5: ~10K points (fast, testing)
  - recursion=6: ~40K points (moderate detail)
  - recursion=7: ~160K points (high detail, slow)
  - recursion=8+: Very slow, use with caution

- **Thread pool sizing**: Engine defaults to `cpu_count // 2` workers
  - Configurable via `WorldGenerationEngine(worker_count=N)`

- **HDF5 compression**: Enabled by default, saves significant disk space

## Project Status

### Implemented
- ✅ Core plugin system with dependency resolution
- ✅ Terrain generation (noise-based elevation)
- ✅ Tectonic simulation (plate boundaries)
- ✅ POI detection
- ✅ HDF5 mesh storage with compression
- ✅ Desktop 3D viewer (PyVista/Qt)
- ✅ Event-driven progress reporting
- ✅ Async execution engine

### TODO
- ⏳ FastAPI REST API (partial implementation)
- ⏳ PostgreSQL metadata storage (partial implementation)
- ⏳ Erosion simulation
- ⏳ Hydrology (rivers, lakes)
- ⏳ Climate modeling
- ⏳ Insolation calculator
- ⏳ Biome generation
- ⏳ Web-based viewer

## Additional Documentation

- `src/README.md` - Detailed architecture overview
- `src/QUICKSTART.md` - Quick start guide
- `src/PLUGIN_DEVELOPMENT_GUIDE.md` - Plugin development tutorial
- `src/tests/README.md` - Testing documentation
- `src/IMPLEMENTATION_SUMMARY.md` - Implementation notes
- `README.md` - Project overview (needs update)
