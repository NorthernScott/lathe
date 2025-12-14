"""Pytest configuration and fixtures."""

import sys
from pathlib import Path
from uuid import uuid4

import pytest
import numpy as np

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lathe.core.engine import WorldGenerationEngine
from lathe.core.events import EventEmitter
from lathe.models.world import World, WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin
from lathe.analysis.poi_detector import POIDetectorPlugin


@pytest.fixture
def world_params():
    """Create basic world parameters for testing."""
    return WorldParameters(
        name="Test World",
        recursion=3,  # Small for fast tests
        seed=42,  # Fixed seed for reproducibility
        ocean_percent=0.55,
    )


@pytest.fixture
def world(world_params):
    """Create a basic world instance."""
    return World(params=world_params)


@pytest.fixture
def world_with_elevation(world):
    """Create a world with pre-populated elevation data."""
    # Add fake elevation data
    elevation = np.random.uniform(-1000, 1000, world.num_points)
    world.add_data_layer("elevation", elevation)

    # Add landforms
    landforms = (elevation > 0).astype(np.float64)
    world.add_data_layer("landforms", landforms)

    return world


@pytest.fixture
def world_with_plates(world_with_elevation):
    """Create a world with elevation and tectonic plates."""
    # Add fake plate data
    plate_id = np.random.randint(0, 12, world_with_elevation.num_points)
    world_with_elevation.add_data_layer("plate_id", plate_id.astype(np.float64))

    return world_with_elevation


@pytest.fixture
def event_emitter():
    """Create a fresh event emitter."""
    return EventEmitter()


@pytest.fixture
def engine():
    """Create a world generation engine."""
    return WorldGenerationEngine()


@pytest.fixture
def engine_with_plugins():
    """Create an engine with all plugins registered."""
    engine = WorldGenerationEngine()
    engine.register_plugin(TerrainGeneratorPlugin())
    engine.register_plugin(TectonicsSimulatorPlugin())
    engine.register_plugin(POIDetectorPlugin())
    return engine


@pytest.fixture
def terrain_plugin():
    """Create a terrain generator plugin."""
    return TerrainGeneratorPlugin()


@pytest.fixture
def tectonics_plugin():
    """Create a tectonics simulator plugin."""
    return TectonicsSimulatorPlugin()


@pytest.fixture
def poi_plugin():
    """Create a POI detector plugin."""
    return POIDetectorPlugin()


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary directory for test data."""
    data_dir = tmp_path / "test_worlds"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def sample_world_id():
    """Generate a sample world ID."""
    return uuid4()


# Pytest hooks for better output
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, no I/O)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, may use I/O)"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests (may take several seconds)"
    )
    config.addinivalue_line(
        "markers", "requires_display: Tests that require a display"
    )
    config.addinivalue_line(
        "markers", "requires_postgres: Tests that require PostgreSQL"
    )
