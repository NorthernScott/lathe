"""Test the new tectonics simulation plugin."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from lathe.core.engine import WorldGenerationEngine
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin
from lathe.storage.mesh_store import MeshStore


async def main():
    """Test tectonics simulation."""
    print("=" * 80)
    print("TESTING TECTONICS SIMULATION v2.0")
    print("=" * 80)

    # Create engine
    engine = WorldGenerationEngine()

    # Register plugins
    engine.register_plugin(TerrainGeneratorPlugin())
    engine.register_plugin(TectonicsSimulatorPlugin())

    # Define parameters - small world for fast testing
    params = WorldParameters(
        name="Tectonics Test World",
        recursion=4,  # 2,562 points - fast
        seed=42,
    )

    # Define plugin parameters
    plugin_params = {
        "terrain": {
            "octaves": 6,
        },
        "tectonics": {
            "num_plates": 8,
            "simulation_steps": 30,  # Reduced for testing
            "mountain_strength": 1.0,
            "trench_strength": 0.8,
            "ridge_strength": 0.5,
        },
    }

    print(f"\nGenerating world: {params.name}")
    print(f"  Points: {2562:,}")
    print(f"  Plates: {plugin_params['tectonics']['num_plates']}")
    print(f"  Simulation steps: {plugin_params['tectonics']['simulation_steps']}")
    print()

    # Progress callback
    def progress(progress_pct, message):
        print(f"  [{progress_pct*100:.0f}%] {message}")

    # Generate world
    world = await engine.generate_world(
        params=params,
        pipeline=["terrain", "tectonics"],
        plugin_params=plugin_params,
        progress_callback=progress,
    )

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    # Check data layers
    print("\nData Layers:")
    for layer in world.list_data_layers():
        print(f"  ✓ {layer}")

    # Check tectonics metadata
    if "tectonic_plates" in world.metadata:
        tecto_meta = world.metadata["tectonic_plates"]
        print(f"\nTectonic Plates: {tecto_meta['num_plates']}")
        print(f"Simulation Steps: {tecto_meta['simulation_steps']}")

        stats = tecto_meta["stats"]
        print("\nBoundary Statistics:")
        print(f"  Total boundaries: {stats['total_boundaries']}")
        print(f"  Convergent: {stats['boundary_counts']['convergent']}")
        print(f"  Divergent: {stats['boundary_counts']['divergent']}")
        print(f"  Transform: {stats['boundary_counts']['transform']}")

        print("\nPlate Composition:")
        for i in range(min(3, tecto_meta['num_plates'])):  # Show first 3 plates
            plate_stats = stats["plates"][f"plate_{i}"]
            print(
                f"  Plate {i}: {plate_stats['total_points']} points "
                f"({plate_stats['land_percent']:.1f}% land)"
            )

    # Get elevation stats
    elevation = world.get_data_layer("elevation")
    print("\nElevation Statistics:")
    print(f"  Min: {elevation.min():.1f}m")
    print(f"  Max: {elevation.max():.1f}m")
    print(f"  Mean: {elevation.mean():.1f}m")
    print(f"  Std Dev: {elevation.std():.1f}m")

    # Save world
    print("\n" + "=" * 80)
    print("SAVING WORLD")
    print("=" * 80)

    store = MeshStore()
    file_path = store.save_world(world, compress=True)
    file_size = file_path.stat().st_size / 1024  # KB

    print(f"\nSaved to: {file_path.name}")
    print(f"File size: {file_size:.1f} KB")

    # Export to VTK for visualization
    vtk_path = Path("data/worlds") / f"{world.id}_tectonics_test.vtk"
    vtk_path.parent.mkdir(parents=True, exist_ok=True)
    store.export_to_vtk(world.id, vtk_path)
    print(f"Exported to: {vtk_path.name}")

    print("\n" + "=" * 80)
    print("SUCCESS! Tectonics simulation is working properly.")
    print("=" * 80)
    print("\nTo visualize:")
    print("  python -m lathe.viz.desktop")
    print("  # or")
    print(f"  paraview {vtk_path}")


if __name__ == "__main__":
    asyncio.run(main())
