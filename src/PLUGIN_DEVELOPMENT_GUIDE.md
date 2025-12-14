# Plugin Development Guide

This guide shows you how to create new simulation and analysis plugins for Lathe.

## Table of Contents
1. [Plugin Types](#plugin-types)
2. [Creating a Simulation Plugin](#creating-a-simulation-plugin)
3. [Creating an Analysis Plugin](#creating-an-analysis-plugin)
4. [Plugin Best Practices](#plugin-best-practices)
5. [Examples](#examples)

---

## Plugin Types

### SimulationPlugin
Modifies the world by adding or updating data layers.

**Examples:**
- Terrain generation (adds elevation data)
- Erosion simulation (modifies elevation)
- Climate modeling (adds temperature, precipitation)

### AnalysisPlugin
Examines the world and extracts information without modifying it.

**Examples:**
- POI detection
- Resource mapping
- Habitability analysis

---

## Creating a Simulation Plugin

### Step 1: Create Plugin File

Create a new file: `src_new/lathe/plugins/<category>/<name>.py`

```python
"""My simulation plugin."""

import asyncio
from typing import Any, Callable

import numpy as np
from numpy.typing import NDArray

from lathe.models.world import World
from lathe.plugins.base import PluginMetadata, PluginResult, SimulationPlugin


class MySimulationPlugin(SimulationPlugin):
    """Short description of what this plugin does."""

    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            name="my_simulation",  # Unique identifier
            version="1.0.0",
            dependencies=["terrain"],  # Plugins that must run first
            description="Detailed description of the simulation",
            author="Your Name",
        )

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
        """Validate parameters before execution.

        Args:
            params: User-provided parameters

        Returns:
            (is_valid, error_message)
        """
        # Example validation
        if "required_param" not in params:
            return False, "required_param is required"

        value = params["required_param"]
        if not isinstance(value, (int, float)) or value <= 0:
            return False, "required_param must be a positive number"

        return True, ""

    def get_required_data_layers(self) -> list[str]:
        """Return list of data layers this plugin needs.

        These must exist before the plugin runs.
        """
        return ["elevation"]  # Example: needs elevation data

    def get_produced_data_layers(self) -> list[str]:
        """Return list of data layers this plugin creates.

        These will be available after the plugin runs.
        """
        return ["my_data"]  # Example: produces my_data layer

    async def execute(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Execute the simulation.

        Args:
            world: World object to modify
            params: Plugin-specific parameters
            progress_callback: Optional callback for progress updates
                               Call with (progress: 0.0-1.0, message: str)

        Returns:
            PluginResult with success status and optional data
        """
        if progress_callback:
            progress_callback(0.0, "Starting simulation")

        # Run CPU-intensive work in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._simulate_sync,
            world,
            params,
            progress_callback,
        )

        if progress_callback:
            progress_callback(1.0, "Simulation complete")

        return result

    def _simulate_sync(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None,
    ) -> PluginResult:
        """Synchronous simulation (runs in thread pool).

        This is where the actual computation happens.
        """
        try:
            # Get required data
            elevation = world.get_data_layer("elevation")
            if elevation is None:
                return PluginResult(
                    success=False,
                    message="Elevation data not found",
                )

            # Report progress
            if progress_callback:
                progress_callback(0.2, "Processing data")

            # Do computation
            # ... your simulation logic here ...
            my_data = np.zeros(world.num_points, dtype=np.float64)

            # Example: simple computation
            for i in range(world.num_points):
                my_data[i] = elevation[i] * 2.0  # Replace with real logic

                # Optional: report progress within loop
                if i % 1000 == 0 and progress_callback:
                    progress = 0.2 + (0.6 * i / world.num_points)
                    progress_callback(progress, f"Processing point {i}/{world.num_points}")

            if progress_callback:
                progress_callback(0.8, "Saving results")

            # Add data to world
            world.add_data_layer("my_data", my_data, overwrite=True)

            if progress_callback:
                progress_callback(0.9, "Computing statistics")

            # Calculate statistics
            stats = {
                "min": float(np.min(my_data)),
                "max": float(np.max(my_data)),
                "mean": float(np.mean(my_data)),
            }

            return PluginResult(
                success=True,
                message=f"Simulation complete: mean={stats['mean']:.2f}",
                data=stats,
            )

        except Exception as e:
            return PluginResult(
                success=False,
                message=f"Simulation failed: {e}",
            )
```

### Step 2: Register Plugin

```python
from lathe.core.engine import WorldGenerationEngine
from lathe.plugins.my_category.my_simulation import MySimulationPlugin

engine = WorldGenerationEngine()
engine.register_plugin(MySimulationPlugin())
```

### Step 3: Use Plugin

```python
world = await engine.generate_world(
    params=params,
    pipeline=["terrain", "my_simulation"],  # Add to pipeline
    plugin_params={
        "my_simulation": {
            "required_param": 42,
        }
    },
)
```

---

## Creating an Analysis Plugin

### Example: Resource Detection

```python
"""Resource detection analysis plugin."""

import asyncio
from typing import Any, Callable
from uuid import uuid4

import numpy as np

from lathe.models.world import World
from lathe.plugins.base import AnalysisPlugin, PluginMetadata, PluginResult


class ResourceDetectorPlugin(AnalysisPlugin):
    """Detects resource-rich locations on the world."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="resource_detector",
            version="1.0.0",
            description="Detects mineral and resource deposits",
            author="Your Name",
        )

    def get_required_data_layers(self) -> list[str]:
        """Requires elevation and plate data."""
        return ["elevation", "plate_id"]

    async def analyze(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Analyze the world for resources."""
        if progress_callback:
            progress_callback(0.0, "Starting resource detection")

        # Run analysis in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._detect_resources_sync,
            world,
            params,
            progress_callback,
        )

        if progress_callback:
            progress_callback(1.0, "Resource detection complete")

        return result

    def _detect_resources_sync(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None,
    ) -> PluginResult:
        """Synchronous resource detection."""
        resources = []

        elevation = world.get_data_layer("elevation")
        plate_id = world.get_data_layer("plate_id")

        if elevation is None or plate_id is None:
            return PluginResult(
                success=False,
                message="Required data layers not found",
            )

        # Detect resources at plate boundaries
        for i in range(world.num_points):
            if progress_callback and i % 1000 == 0:
                progress = i / world.num_points
                progress_callback(progress, f"Scanning point {i}/{world.num_points}")

            # Check neighbors for plate boundaries
            neighbors = world.get_neighbors(i, radius=10000)  # 10km
            if len(neighbors) > 0:
                # Plate boundary if neighboring plates differ
                neighbor_plates = plate_id[neighbors]
                if len(np.unique(neighbor_plates)) > 1:
                    # Potential resource at boundary
                    resources.append({
                        "id": str(uuid4()),
                        "type": "mineral",
                        "location": tuple(world.mesh.points[i]),
                        "mesh_index": i,
                        "elevation": float(elevation[i]),
                        "plate_id": int(plate_id[i]),
                    })

        return PluginResult(
            success=True,
            message=f"Found {len(resources)} resource locations",
            data={"resources": resources, "count": len(resources)},
        )
```

---

## Plugin Best Practices

### 1. Progress Reporting

Always report progress for long-running operations:

```python
if progress_callback:
    progress_callback(0.5, "Halfway done")
```

Report at:
- Start (0.0)
- Major milestones (0.25, 0.5, 0.75)
- Completion (1.0)

### 2. Error Handling

Always wrap execution in try/except:

```python
try:
    # Your logic
    return PluginResult(success=True, message="Success")
except Exception as e:
    return PluginResult(success=False, message=f"Failed: {e}")
```

### 3. Parameter Validation

Validate all parameters:

```python
def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
    if "required_param" not in params:
        return False, "required_param is required"

    if params["required_param"] < 0:
        return False, "required_param must be non-negative"

    return True, ""
```

### 4. Data Layer Management

Declare required and produced layers:

```python
def get_required_data_layers(self) -> list[str]:
    return ["elevation"]  # What we need

def get_produced_data_layers(self) -> list[str]:
    return ["my_data"]  # What we produce
```

### 5. Async Execution

Use thread pool for CPU-intensive work:

```python
async def execute(self, world, params, progress_callback):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        self._heavy_computation,
        world,
        params,
    )
```

### 6. Statistics and Metadata

Return useful statistics:

```python
stats = {
    "min": float(np.min(data)),
    "max": float(np.max(data)),
    "mean": float(np.mean(data)),
    "features_found": len(features),
}

return PluginResult(
    success=True,
    message="Complete",
    data=stats,
)
```

---

## Examples

### Erosion Plugin Template

```python
class ErosionPlugin(SimulationPlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="erosion",
            version="1.0.0",
            dependencies=["terrain", "hydrology"],
            description="Simulates hydraulic and thermal erosion",
        )

    def get_required_data_layers(self) -> list[str]:
        return ["elevation", "water_flow"]

    def get_produced_data_layers(self) -> list[str]:
        return ["erosion_amount", "sediment"]

    async def execute(self, world, params, progress_callback):
        # Implement erosion simulation
        pass
```

### Climate Plugin Template

```python
class ClimatePlugin(SimulationPlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="climate",
            version="1.0.0",
            dependencies=["terrain", "insolation"],
            description="Models temperature and precipitation",
        )

    def get_required_data_layers(self) -> list[str]:
        return ["elevation", "insolation", "latitude"]

    def get_produced_data_layers(self) -> list[str]:
        return ["temperature", "precipitation", "humidity"]

    async def execute(self, world, params, progress_callback):
        # Implement climate modeling
        pass
```

---

## Testing Your Plugin

### Unit Test Template

```python
import pytest
from lathe.models.world import WorldParameters, World
from lathe.plugins.my_category.my_plugin import MyPlugin

@pytest.mark.asyncio
async def test_my_plugin():
    # Create test world
    world = World(WorldParameters(recursion=3))  # Small for testing

    # Add required data layers
    world.add_data_layer("elevation", np.random.rand(world.num_points))

    # Create and execute plugin
    plugin = MyPlugin()
    result = await plugin.execute(world, {}, None)

    # Assert results
    assert result.success
    assert world.has_data_layer("my_data")
    assert len(world.get_data_layer("my_data")) == world.num_points
```

### Integration Test

```python
from lathe.core.engine import WorldGenerationEngine

async def test_plugin_in_pipeline():
    engine = WorldGenerationEngine()
    engine.register_plugin(TerrainGeneratorPlugin())
    engine.register_plugin(MyPlugin())

    world = await engine.generate_world(
        params=WorldParameters(recursion=3),
        pipeline=["terrain", "my_plugin"],
    )

    assert world.has_data_layer("my_data")
```

---

## Debugging Tips

### Enable Detailed Logging

```python
from lathe.core.events import get_global_emitter, EventType

emitter = get_global_emitter()

def log_all(event):
    print(f"[{event.type.value}] {event.message}")
    if event.data:
        print(f"  Data: {event.data}")

emitter.subscribe(None, log_all)  # Subscribe to all events
```

### Check Data Layers

```python
print(f"Available layers: {world.list_data_layers()}")
print(f"Has elevation: {world.has_data_layer('elevation')}")

data = world.get_data_layer("elevation")
print(f"Elevation stats: min={data.min()}, max={data.max()}")
```

### Validate Dependencies

```python
# Engine will validate automatically, but you can check manually:
required = plugin.get_required_data_layers()
missing = [layer for layer in required if not world.has_data_layer(layer)]
if missing:
    print(f"Missing layers: {missing}")
```

---

## Next Steps

1. **Study existing plugins:**
   - `lathe/plugins/terrain/generator.py`
   - `lathe/plugins/tectonics/simulator.py`
   - `lathe/analysis/poi_detector.py`

2. **Start simple:**
   - Create a basic plugin with minimal logic
   - Test it thoroughly
   - Add features incrementally

3. **Follow the pattern:**
   - Use the templates above
   - Follow best practices
   - Report progress
   - Handle errors

4. **Contribute:**
   - Share your plugins
   - Document thoroughly
   - Write tests

Happy plugin development! 🚀
