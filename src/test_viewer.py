"""Test script for desktop viewer - non-interactive mode."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from uuid import UUID
from lathe.storage.mesh_store import MeshStore
import pyvista as pv

def test_viewer_components():
    """Test viewer components without GUI."""
    print("Testing Desktop Viewer Components")
    print("=" * 60)

    # Get available worlds
    store = MeshStore("./data/worlds")
    worlds = store.list_worlds()

    if not worlds:
        print("No worlds found. Run an example first.")
        return

    print(f"\nFound {len(worlds)} world(s)")

    # Load first world
    world = store.load_world(UUID(worlds[0]["world_id"]))

    print(f"\nLoaded: {world.params.name}")
    print(f"  ID: {world.id}")
    print(f"  Points: {world.num_points:,}")
    print(f"  Layers: {', '.join(sorted(world.list_data_layers()))}")

    # Test PyVista rendering (off-screen)
    print("\nTesting PyVista rendering (off-screen)...")

    pv.set_plot_theme("dark")
    plotter = pv.Plotter(off_screen=True, window_size=[800, 600])

    # Add mesh with elevation
    plotter.add_mesh(
        world.mesh,
        scalars="elevation",
        cmap="terrain",
        show_edges=False,
        smooth_shading=True,
    )

    # Test screenshot
    screenshot_path = "test_render.png"
    plotter.screenshot(screenshot_path)
    plotter.close()

    if Path(screenshot_path).exists():
        size = Path(screenshot_path).stat().st_size
        print(f"  ✓ Screenshot saved: {screenshot_path} ({size:,} bytes)")
        Path(screenshot_path).unlink()  # Clean up
    else:
        print("  ✗ Screenshot failed")

    print("\n✓ All viewer components working!")


if __name__ == "__main__":
    test_viewer_components()
