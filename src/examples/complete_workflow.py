"""Complete workflow example: Generate -> Analyze -> Store -> Visualize."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import lathe
sys.path.insert(0, str(Path(__file__).parent.parent))

from lathe.analysis.poi_detector import POIDetectorPlugin
from lathe.core.engine import WorldGenerationEngine
from lathe.core.events import Event, EventType, get_global_emitter
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin
from lathe.storage.mesh_store import MeshStore


class ProgressBar:
    """Simple console progress bar."""

    def __init__(self, total_width=50):
        self.total_width = total_width
        self.current_plugin = ""
        self.current_progress = 0.0

    def update(self, plugin: str, progress: float, message: str):
        """Update progress bar."""
        self.current_plugin = plugin
        self.current_progress = progress

        filled = int(self.total_width * progress)
        bar = "█" * filled + "░" * (self.total_width - filled)

        print(f"\r{plugin:12} [{bar}] {progress:.1%} - {message}", end="", flush=True)

    def complete(self):
        """Mark as complete."""
        print()  # New line


async def main():
    """Run complete workflow."""
    print("=" * 70)
    print(" " * 15 + "LATHE WORLD GENERATION")
    print(" " * 10 + "Complete Workflow Demonstration")
    print("=" * 70)

    # Set up progress tracking
    progress_bar = ProgressBar()
    emitter = get_global_emitter()

    def on_plugin_start(event: Event):
        plugin = event.data.get("plugin", "unknown")
        print(f"\n▶ Starting: {plugin}")

    def on_plugin_progress(event: Event):
        plugin = event.data.get("plugin", "unknown")
        progress = event.data.get("progress", 0.0)
        progress_bar.update(plugin, progress, event.message)

    def on_plugin_complete(event: Event):
        plugin = event.data.get("plugin", "unknown")
        progress_bar.complete()
        print(f"✓ Completed: {plugin}")

    emitter.subscribe(EventType.PLUGIN_STARTED, on_plugin_start)
    emitter.subscribe(EventType.PLUGIN_PROGRESS, on_plugin_progress)
    emitter.subscribe(EventType.PLUGIN_COMPLETED, on_plugin_complete)

    # ========================================================================
    # STEP 1: Initialize Engine
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 1: Initializing Engine")
    print("─" * 70)

    engine = WorldGenerationEngine(max_workers=4)

    # Register plugins
    plugins = [
        TerrainGeneratorPlugin(),
        TectonicsSimulatorPlugin(),
        POIDetectorPlugin(),
    ]

    for plugin in plugins:
        engine.register_plugin(plugin)
        print(f"  ✓ Registered: {plugin.metadata.name}")

    # ========================================================================
    # STEP 2: Configure World
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 2: Configuring World Parameters")
    print("─" * 70)

    params = WorldParameters(
        name="Demo World Alpha",
        recursion=5,  # 10,242 points
        seed=12345,
        ocean_percent=0.60,
        zmax=8848,  # Everest height
        zmin=-11034,  # Mariana Trench depth
        zscale=25.0,
    )

    print(f"  Name:         {params.name}")
    print(f"  Recursion:    {params.recursion}")
    print(f"  Seed:         {params.seed}")
    print(f"  Ocean %:      {params.ocean_percent * 100:.0f}%")
    print(f"  Elevation:    {params.zmin} m to {params.zmax} m")

    # ========================================================================
    # STEP 3: Generate World
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 3: Generating World")
    print("─" * 70)

    pipeline = ["terrain", "tectonics"]
    plugin_params = {
        "terrain": {
            "octaves": 8,
            "init_roughness": 1.5,
            "init_strength": 0.4,
            "roughness": 2.5,
            "persistence": 0.5,
        },
        "tectonics": {"num_plates": 15},
    }

    print(f"\nPipeline: {' → '.join(pipeline)}")
    print("\nStarting generation...")

    world = await engine.generate_world(
        params=params,
        pipeline=pipeline,
        plugin_params=plugin_params,
    )

    print("\n✓ World generated successfully!")

    # ========================================================================
    # STEP 4: Analyze Statistics
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 4: Analyzing World Statistics")
    print("─" * 70)

    print(f"\nWorld ID:      {world.id}")
    print(f"Mesh Points:   {world.num_points:,}")
    print(f"Mesh Faces:    {world.num_faces:,}")

    print("\nData Layers:")
    for layer in world.list_data_layers():
        print(f"  • {layer}")

    # Elevation stats
    elevation = world.get_data_layer("elevation")
    if elevation is not None:
        print("\nElevation Statistics:")
        print(f"  Minimum:      {elevation.min():,.1f} m")
        print(f"  Maximum:      {elevation.max():,.1f} m")
        print(f"  Mean:         {elevation.mean():,.1f} m")
        print(f"  Std Dev:      {elevation.std():,.1f} m")

    # Land/ocean distribution
    landforms = world.get_data_layer("landforms")
    if landforms is not None:
        land_pct = (landforms.sum() / len(landforms)) * 100
        print("\nLand Distribution:")
        print(f"  Land:         {land_pct:.1f}%")
        print(f"  Ocean:        {100 - land_pct:.1f}%")

    # Tectonic plates
    plate_id = world.get_data_layer("plate_id")
    if plate_id is not None:
        num_plates = int(plate_id.max()) + 1
        print(f"\nTectonic Plates:  {num_plates}")

    # ========================================================================
    # STEP 5: Detect Points of Interest
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 5: Detecting Points of Interest")
    print("─" * 70)

    print("\nRunning POI detection...")

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
                "min_importance": 0.5,
            }
        },
    )

    if "poi_detector" in results:
        poi_data = results["poi_detector"].data
        pois = poi_data.get("pois", [])

        print(f"\n✓ Found {len(pois)} points of interest")

        # Group by type
        by_type = {}
        for poi in pois:
            poi_type = poi["type"]
            if poi_type not in by_type:
                by_type[poi_type] = []
            by_type[poi_type].append(poi)

        print("\nPOI Breakdown:")
        for poi_type, type_pois in sorted(by_type.items()):
            print(f"  {poi_type.capitalize():15} {len(type_pois):3}")

        # Show most important POIs
        print("\nTop 10 Most Important POIs:")
        sorted_pois = sorted(pois, key=lambda p: p["importance"], reverse=True)[:10]

        for i, poi in enumerate(sorted_pois, 1):
            imp_bar = "█" * int(poi["importance"] * 20)
            print(f"  {i:2}. {poi['name']:25} ({poi['type']:10}) {imp_bar} {poi['importance']:.2f}")

    # ========================================================================
    # STEP 6: Save World
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 6: Saving World to Disk")
    print("─" * 70)

    mesh_store = MeshStore(storage_dir="./data/worlds")

    print("\nSaving world to HDF5...")
    hdf5_path = mesh_store.save_world(world, compress=True)

    file_size_mb = hdf5_path.stat().st_size / (1024 * 1024)
    print(f"✓ Saved to: {hdf5_path}")
    print(f"  File size:   {file_size_mb:.2f} MB")
    print("  Compressed:  Yes")

    # Verify save
    print("\nVerifying save...")
    loaded = mesh_store.load_world(world.id)
    print(f"✓ Successfully loaded world: {loaded.params.name}")
    print(f"  Points match: {loaded.num_points == world.num_points}")
    print(f"  Layers match: {set(loaded.list_data_layers()) == set(world.list_data_layers())}")

    # ========================================================================
    # STEP 7: Export Options
    # ========================================================================
    print("\n" + "─" * 70)
    print("STEP 7: Export Options")
    print("─" * 70)

    # Export to VTK
    vtk_path = Path(f"./data/worlds/world_{world.id}.vtk")
    mesh_store.export_to_vtk(world.id, vtk_path)
    vtk_size_mb = vtk_path.stat().st_size / (1024 * 1024)
    print(f"\n✓ Exported to VTK: {vtk_path}")
    print(f"  File size:   {vtk_size_mb:.2f} MB")
    print("  Use with:    ParaView, VTK-compatible viewers")

    # ========================================================================
    # STEP 8: Summary
    # ========================================================================
    print("\n" + "=" * 70)
    print(" " * 25 + "GENERATION COMPLETE")
    print("=" * 70)

    print("\nWorld Summary:")
    print(f"  Name:        {world.params.name}")
    print(f"  ID:          {world.id}")
    print(f"  Points:      {world.num_points:,}")
    print(f"  Plates:      {num_plates if plate_id is not None else 'N/A'}")
    print(f"  POIs:        {len(pois) if 'pois' in poi_data else 0}")
    print(f"  Storage:     {file_size_mb:.2f} MB")

    print("\nGeneration Metadata:")
    print(f"  Time:        {world.metadata.get('generation_time_seconds', 0):.2f} seconds")
    print(f"  Pipeline:    {' → '.join(world.metadata.get('pipeline_steps', []))}")

    print("\nNext Steps:")
    print(f"  1. View in 3D:    python -m lathe.viz.desktop {world.id}")
    print("  2. Start API:     python -m lathe.api.server")
    print(f"  3. Open VTK:      paraview {vtk_path}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
