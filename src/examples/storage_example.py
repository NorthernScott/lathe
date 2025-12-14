"""Example demonstrating world storage and loading."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import lathe
sys.path.insert(0, str(Path(__file__).parent.parent))

from lathe.core.engine import WorldGenerationEngine
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.storage.mesh_store import MeshStore


async def generate_and_save_world():
    """Generate a world and save it to both HDF5 and PostgreSQL."""
    print("=" * 60)
    print("World Storage Example - Generation & Saving")
    print("=" * 60)

    # Create engine and register plugins
    engine = WorldGenerationEngine()
    engine.register_plugin(TerrainGeneratorPlugin())

    # Create stores
    mesh_store = MeshStore(storage_dir="./data/worlds")
    # Note: Update database URL for your PostgreSQL setup
    # metadata_store = MetadataStore(database_url="postgresql://user:password@localhost/lathe")

    # Generate a simple world
    params = WorldParameters(
        name="Persistent World",
        recursion=4,  # Small for quick generation
        seed=123,
    )

    print(f"\nGenerating world: {params.name}...")
    world = await engine.generate_world(
        params=params,
        pipeline=["terrain"],
    )

    print(f"World generated: {world.id}")
    print(f"  Points: {world.num_points:,}")
    print(f"  Layers: {', '.join(world.list_data_layers())}")

    # Save to HDF5
    print("\nSaving to HDF5...")
    hdf5_path = mesh_store.save_world(world, compress=True)
    print(f"  Saved to: {hdf5_path}")
    print(f"  Size: {hdf5_path.stat().st_size / 1024:.1f} KB")

    # Save metadata to PostgreSQL (commented out - requires PostgreSQL)
    # print("\nSaving metadata to PostgreSQL...")
    # metadata_store.create_tables()  # Create tables if they don't exist
    # metadata_store.save_world_metadata(
    #     world_id=world.id,
    #     name=world.params.name,
    #     hdf5_path=str(hdf5_path),
    #     parameters=world.params.__dict__,
    #     metadata=world.metadata,
    # )
    # print("  Metadata saved")

    return world.id


def load_and_inspect_world(world_id):
    """Load a saved world and inspect it."""
    print("\n" + "=" * 60)
    print("World Storage Example - Loading & Inspection")
    print("=" * 60)

    mesh_store = MeshStore(storage_dir="./data/worlds")

    # Check if world exists
    if not mesh_store.world_exists(world_id):
        print(f"World {world_id} not found!")
        return

    # Get world info without loading full mesh
    print("\nFetching world info...")
    info = mesh_store.get_world_info(world_id)

    if info:
        print(f"\nWorld: {info['name']}")
        print(f"  ID: {info['world_id']}")
        print(f"  Points: {info['num_points']:,}")
        print(f"  Layers: {', '.join(info['data_layers'])}")
        print(f"  File size: {info['file_size_mb']:.2f} MB")
        print("\nParameters:")
        for key, value in info["parameters"].items():
            print(f"  {key}: {value}")

    # Load full world
    print("\nLoading full world from HDF5...")
    world = mesh_store.load_world(world_id)

    print(f"World loaded: {world.params.name}")
    print(f"  Mesh points: {world.num_points:,}")
    print(f"  Data layers: {', '.join(world.list_data_layers())}")

    # Access a specific data layer
    print("\nLoading specific data layer...")
    elevation = mesh_store.get_data_layer(world_id, "elevation")

    if elevation is not None:
        print("Elevation layer:")
        print(f"  Shape: {elevation.shape}")
        print(f"  Min: {elevation.min():.1f} m")
        print(f"  Max: {elevation.max():.1f} m")
        print(f"  Mean: {elevation.mean():.1f} m")

    # Export to VTK for use in ParaView or other tools
    print("\nExporting to VTK format...")
    vtk_path = f"./data/worlds/world_{world_id}.vtk"
    mesh_store.export_to_vtk(world_id, vtk_path)
    print(f"  Exported to: {vtk_path}")


def list_all_worlds():
    """List all saved worlds."""
    print("\n" + "=" * 60)
    print("All Saved Worlds")
    print("=" * 60)

    mesh_store = MeshStore(storage_dir="./data/worlds")
    worlds = mesh_store.list_worlds()

    if not worlds:
        print("No worlds found.")
        return

    print(f"\nFound {len(worlds)} world(s):\n")

    for world in worlds:
        print(f"  {world['name']}")
        print(f"    ID: {world['world_id']}")
        print(f"    Points: {world['num_points']:,}")
        print(f"    Size: {world['file_size_mb']:.2f} MB")
        print(f"    Layers: {', '.join(world['data_layers'])}")
        print()


async def main():
    """Run storage examples."""
    # Generate and save a world
    world_id = await generate_and_save_world()

    # Load and inspect it
    load_and_inspect_world(world_id)

    # List all worlds
    list_all_worlds()

    print("\n" + "=" * 60)
    print("Storage example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
