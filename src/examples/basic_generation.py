"""Basic example of world generation using the new architecture."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import lathe
sys.path.insert(0, str(Path(__file__).parent.parent))

from lathe.analysis.poi_detector import POIDetectorPlugin
from lathe.core.engine import WorldGenerationEngine
from lathe.core.events import Event, get_global_emitter
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin
from lathe.storage.mesh_store import MeshStore


def setup_event_logging():
    """Set up event logging to print progress."""
    emitter = get_global_emitter()

    def log_event(event: Event):
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"[{timestamp}] {event.type.value}: {event.message}")

    # Subscribe to all events
    emitter.subscribe(None, log_event)


async def main():
    """Generate a simple world."""
    print("=" * 60)
    print("Lathe World Generation - Basic Example")
    print("=" * 60)

    # Set up event logging
    setup_event_logging()

    # Create engine
    engine = WorldGenerationEngine(workers=4)

    # Register plugins
    print("\nRegistering plugins...")
    engine.register_plugin(TerrainGeneratorPlugin())
    engine.register_plugin(TectonicsSimulatorPlugin())
    engine.register_plugin(POIDetectorPlugin())

    print(f"Registered plugins: {engine.list_plugins()}")

    # Define world parameters
    params = WorldParameters(
        name="Example World",
        recursion=5,  # Lower for faster generation
        seed=42,  # Fixed seed for reproducibility
        ocean_percent=0.55,
    )

    print(f"\nGenerating world: {params.name}")
    print(f"  Recursion: {params.recursion} ({params.radius} m radius)")
    print(f"  Seed: {params.seed}")

    # Define generation pipeline
    pipeline = ["terrain", "tectonics"]

    # Plugin parameters
    plugin_params = {
        "terrain": {"octaves": 8, "roughness": 2.5, "persistence": 0.5},
        "tectonics": {"num_plates": 12},
    }

    # Generate world
    print("\n" + "=" * 60)
    print("Starting generation...")
    print("=" * 60)

    world = await engine.generate_world(
        params=params,
        pipeline=pipeline,
        plugin_params=plugin_params,
    )

    print("\n" + "=" * 60)
    print("World generation complete!")
    print("=" * 60)

    # Print world statistics
    print(f"\nWorld ID: {world.id}")
    print(f"Name: {world.params.name}")
    print(f"Mesh points: {world.num_points:,}")
    print(f"Mesh faces: {world.num_faces:,}")
    print(f"Data layers: {', '.join(world.list_data_layers())}")

    # Get elevation statistics
    elevation = world.get_data_layer("elevation")
    if elevation is not None:
        print("\nElevation statistics:")
        print(f"  Min: {elevation.min():.1f} m")
        print(f"  Max: {elevation.max():.1f} m")
        print(f"  Mean: {elevation.mean():.1f} m")

    landforms = world.get_data_layer("landforms")
    if landforms is not None:
        land_percent = (landforms.sum() / len(landforms)) * 100
        print("\nLandforms:")
        print(f"  Land: {land_percent:.1f}%")
        print(f"  Ocean: {100 - land_percent:.1f}%")

    # Save world to HDF5
    print("\n" + "=" * 60)
    print("Saving world to HDF5...")
    print("=" * 60)

    mesh_store = MeshStore(storage_dir="./data/worlds")
    hdf5_path = mesh_store.save_world(world, compress=True)

    print(f"Saved to: {hdf5_path}")
    print(f"File size: {hdf5_path.stat().st_size / (1024 * 1024):.2f} MB")

    # Run POI analysis
    print("\n" + "=" * 60)
    print("Analyzing Points of Interest...")
    print("=" * 60)

    results = await engine.analyze_world(
        world=world,
        analyzers=["poi_detector"],
        analyzer_params={
            "poi_detector": {
                "detect_mountains": True,
                "detect_valleys": True,
                "detect_coastlines": True,
                "detect_settlements": True,
                "detect_viewpoints": True,
                "min_importance": 0.6,
            }
        },
    )

    if "poi_detector" in results:
        poi_data = results["poi_detector"].data
        pois = poi_data.get("pois", [])

        print(f"\nFound {len(pois)} POIs:")

        # Group by type
        by_type = {}
        for poi in pois:
            poi_type = poi["type"]
            if poi_type not in by_type:
                by_type[poi_type] = []
            by_type[poi_type].append(poi)

        for poi_type, type_pois in by_type.items():
            print(f"  {poi_type.capitalize()}: {len(type_pois)}")

        # Show top 5 most important POIs
        print("\nTop 5 most important POIs:")
        sorted_pois = sorted(pois, key=lambda p: p["importance"], reverse=True)[:5]
        for i, poi in enumerate(sorted_pois, 1):
            print(f"  {i}. {poi['name']} ({poi['type']})")
            print(f"     Importance: {poi['importance']:.2f}")
            print(f"     Properties: {poi['properties']}")

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
