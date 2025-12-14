# Lathe Test Suite

Comprehensive test suite for the Lathe world generation system using pytest.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures for all tests
├── unit/                    # Unit tests (fast, no I/O)
│   ├── test_world.py       # World model tests
│   ├── test_events.py      # Event system tests
│   ├── test_engine.py      # Engine orchestration tests
│   ├── test_terrain_plugin.py       # Terrain plugin tests
│   ├── test_tectonics_plugin.py     # Tectonics plugin tests
│   ├── test_poi_detector.py         # POI detector tests
│   ├── test_mesh_store.py           # HDF5 storage tests
│   └── test_metadata_store.py       # PostgreSQL storage tests
└── integration/             # Integration tests (slower)
    └── test_complete_workflow.py    # End-to-end workflow tests
```

## Running Tests

### Run all tests
```bash
cd src_new
pytest
```

### Run only unit tests (fast)
```bash
pytest -m unit
```

### Run only integration tests
```bash
pytest -m integration
```

### Run tests with coverage
```bash
pytest --cov=lathe --cov-report=html
```

### Run specific test file
```bash
pytest tests/unit/test_world.py
```

### Run specific test
```bash
pytest tests/unit/test_world.py::TestWorld::test_world_initialization
```

### Run tests in parallel (requires pytest-xdist)
```bash
pytest -n auto
```

## Test Markers

Tests are categorized with markers:

- `@pytest.mark.unit` - Unit tests (fast, no I/O)
- `@pytest.mark.integration` - Integration tests (slower, may use I/O)
- `@pytest.mark.slow` - Slow tests (may take several seconds)
- `@pytest.mark.requires_display` - Tests requiring GUI/display
- `@pytest.mark.requires_postgres` - Tests requiring PostgreSQL

### Skip slow tests
```bash
pytest -m "not slow"
```

### Skip PostgreSQL tests
```bash
pytest -m "not requires_postgres"
```

### Run only display tests
```bash
pytest -m requires_display
```

## Fixtures

Common fixtures available in all tests (defined in `conftest.py`):

### World Fixtures
- `world_params` - Basic WorldParameters for testing
- `world` - World instance (recursion=3, seed=42)
- `world_with_elevation` - World with elevation data
- `world_with_plates` - World with elevation and tectonic plates

### Component Fixtures
- `event_emitter` - Fresh EventEmitter instance
- `engine` - WorldGenerationEngine instance
- `engine_with_plugins` - Engine with all plugins registered

### Plugin Fixtures
- `terrain_plugin` - TerrainGeneratorPlugin instance
- `tectonics_plugin` - TectonicsSimulatorPlugin instance
- `poi_plugin` - POIDetectorPlugin instance

### Utility Fixtures
- `temp_data_dir` - Temporary directory for test data
- `sample_world_id` - UUID for testing

## Writing New Tests

### Unit Test Template

```python
"""Unit tests for MyComponent."""

import pytest
from lathe.my_module import MyComponent


@pytest.mark.unit
class TestMyComponent:
    """Test MyComponent class."""

    def test_initialization(self):
        """Test component initialization."""
        component = MyComponent()
        assert component is not None

    def test_some_method(self):
        """Test some method."""
        component = MyComponent()
        result = component.some_method()
        assert result == expected_value
```

### Async Test Template

```python
@pytest.mark.asyncio
async def test_async_function(self, world):
    """Test async function."""
    result = await some_async_function(world)
    assert result.success is True
```

### Integration Test Template

```python
@pytest.mark.integration
class TestIntegrationScenario:
    """Test integration scenario."""

    @pytest.mark.asyncio
    async def test_complete_workflow(self, engine_with_plugins):
        """Test complete workflow."""
        world = await engine_with_plugins.generate_world(...)
        # ... test the complete workflow
```

## Test Coverage

To generate an HTML coverage report:

```bash
pytest --cov=lathe --cov-report=html
open htmlcov/index.html
```

Current test coverage targets:
- Core modules: 90%+
- Plugins: 80%+
- Storage: 80%+
- Overall: 85%+

## Continuous Integration

Tests are designed to run in CI environments:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd src_new
    pytest -v --cov=lathe
```

## Troubleshooting

### Import errors
Make sure you're running tests from the `src_new` directory:
```bash
cd src_new
pytest
```

### Missing dependencies
Install test dependencies:
```bash
uv pip install -e ".[dev]"
```

### PostgreSQL tests failing
PostgreSQL tests require a running database. Skip them if not needed:
```bash
pytest -m "not requires_postgres"
```

### Display tests failing
Display tests require X11/GUI. Skip them on headless systems:
```bash
pytest -m "not requires_display"
```

## Best Practices

1. **Fast tests**: Keep unit tests fast (< 1 second each)
2. **Isolated**: Each test should be independent
3. **Clear names**: Use descriptive test names
4. **One assertion focus**: Test one thing per test
5. **Use fixtures**: Reuse common setup via fixtures
6. **Mark appropriately**: Use markers to categorize tests
7. **Document**: Add docstrings to test functions

## Performance

Current test suite performance (approximate):

- Unit tests: ~10-20 seconds
- Integration tests: ~30-60 seconds
- Full suite: ~60-90 seconds

Running with `-n auto` (parallel execution) can reduce this by 50-70%.
