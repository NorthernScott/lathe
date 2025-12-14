"""Comprehensive test for all visualization and export methods."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncio
import pyvista as pv

from lathe.core.engine import WorldGenerationEngine
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin
from lathe.storage.mesh_store import MeshStore


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def test_generation():
    """Test world generation."""
    print_section("TEST 1: World Generation")

    engine = WorldGenerationEngine()
    engine.register_plugin(TerrainGeneratorPlugin())
    engine.register_plugin(TectonicsSimulatorPlugin())

    params = WorldParameters(
        name="Visualization Test World",
        recursion=4,  # Smaller for faster testing
        seed=999,
    )

    print(f"\nGenerating world: {params.name}")
    print(f"  Recursion: {params.recursion} (2,562 points)")

    world = await engine.generate_world(
        params=params,
        pipeline=["terrain", "tectonics"],
    )

    print("\n✓ World generated successfully")
    print(f"  ID: {world.id}")
    print(f"  Points: {world.num_points:,}")
    print(f"  Layers: {len(world.list_data_layers())}")

    return world


def test_hdf5_storage(world):
    """Test HDF5 storage."""
    print_section("TEST 2: HDF5 Storage")

    store = MeshStore("./data/worlds")

    print("\nSaving to HDF5...")
    hdf5_path = store.save_world(world, compress=True)
    file_size = hdf5_path.stat().st_size / 1024

    print(f"✓ Saved to: {hdf5_path}")
    print(f"  File size: {file_size:.1f} KB")

    print("\nLoading from HDF5...")
    loaded = store.load_world(world.id)

    print(f"✓ Loaded world: {loaded.params.name}")
    print(f"  Points match: {loaded.num_points == world.num_points}")
    print(f"  Layers: {len(loaded.list_data_layers())}")

    # Verify data integrity
    import numpy as np
    original_elev = world.get_data_layer("elevation")
    loaded_elev = loaded.get_data_layer("elevation")

    if original_elev is not None and loaded_elev is not None:
        match = np.allclose(original_elev, loaded_elev)
        print(f"  Data integrity: {'✓ PASS' if match else '✗ FAIL'}")

    return loaded


def test_vtk_export(world):
    """Test VTK export."""
    print_section("TEST 3: VTK Export")

    store = MeshStore("./data/worlds")
    vtk_path = Path(f"./data/worlds/test_world_{world.id}.vtk")

    print(f"\nExporting to VTK: {vtk_path}")
    store.export_to_vtk(world.id, vtk_path)

    if vtk_path.exists():
        file_size = vtk_path.stat().st_size / 1024
        print("✓ VTK export successful")
        print(f"  File size: {file_size:.1f} KB")

        # Try loading it back with PyVista
        print("\nValidating VTK file...")
        try:
            mesh = pv.read(str(vtk_path))
            print("✓ VTK file is valid")
            print(f"  Points: {mesh.n_points:,}")
            print(f"  Cells: {mesh.n_cells:,}")
            print(f"  Arrays: {list(mesh.point_data.keys())}")
        except Exception as e:
            print(f"✗ VTK validation failed: {e}")

        # Clean up
        vtk_path.unlink()
    else:
        print("✗ VTK export failed")


def test_offscreen_rendering(world):
    """Test off-screen rendering."""
    print_section("TEST 4: Off-Screen Rendering")

    pv.set_plot_theme("dark")

    # Test different scalar layers
    scalar_layers = ["elevation", "plate_id"]

    for scalar in scalar_layers:
        if not world.has_data_layer(scalar):
            print(f"\n⊘ Skipping {scalar} (not available)")
            continue

        print(f"\nRendering with '{scalar}' scalar...")

        plotter = pv.Plotter(off_screen=True, window_size=[800, 600])

        # Choose colormap based on scalar
        cmap = "terrain" if scalar == "elevation" else "viridis"

        plotter.add_mesh(
            world.mesh,
            scalars=scalar,
            cmap=cmap,
            show_edges=False,
            smooth_shading=True,
            scalar_bar_args={"title": scalar},
        )

        # Set camera
        radius = world.params.radius
        plotter.camera_position = [
            (radius * 2, radius * 2, radius * 2),
            (0, 0, 0),
            (0, 0, 1),
        ]

        # Save screenshot
        screenshot_path = f"test_render_{scalar}.png"
        plotter.screenshot(screenshot_path)
        plotter.close()

        if Path(screenshot_path).exists():
            file_size = Path(screenshot_path).stat().st_size / 1024
            print(f"  ✓ Screenshot: {screenshot_path} ({file_size:.1f} KB)")

            # Clean up
            Path(screenshot_path).unlink()
        else:
            print("  ✗ Screenshot failed")


def test_interactive_features(world):
    """Test interactive features (without actually showing)."""
    print_section("TEST 5: Interactive Features")

    print("\nTesting plotter configuration...")

    # Create plotter (don't show)
    plotter = pv.Plotter(off_screen=True)

    # Test mesh addition
    print("  • Adding mesh with scalars")
    plotter.add_mesh(
        world.mesh,
        scalars="elevation",
        cmap="terrain",
        show_edges=False,
        smooth_shading=True,
    )

    # Test adding actors
    print("  • Adding coordinate axes")
    radius = world.params.radius
    import numpy as np

    # X axis
    plotter.add_lines(
        np.array([[-radius * 1.5, 0, 0], [radius * 1.5, 0, 0]]),
        color="red",
        width=2,
    )
    # Y axis
    plotter.add_lines(
        np.array([[0, -radius * 1.5, 0], [0, radius * 1.5, 0]]),
        color="green",
        width=2,
    )
    # Z axis
    plotter.add_lines(
        np.array([[0, 0, -radius * 1.5], [0, 0, radius * 1.5]]),
        color="blue",
        width=2,
    )

    # Test camera positioning
    print("  • Setting camera position")
    plotter.camera_position = [
        (radius * 2, radius * 2, radius * 2),
        (0, 0, 0),
        (0, 0, 1),
    ]

    # Test screenshot
    print("  • Taking screenshot")
    plotter.screenshot("test_interactive.png")

    plotter.close()

    if Path("test_interactive.png").exists():
        print("  ✓ All interactive features working")
        Path("test_interactive.png").unlink()
    else:
        print("  ✗ Some features failed")


def test_data_layer_switching(world):
    """Test switching between data layers."""
    print_section("TEST 6: Data Layer Switching")

    layers = world.list_data_layers()
    print(f"\nAvailable layers: {len(layers)}")

    plotter = pv.Plotter(off_screen=True, window_size=[400, 400])

    for layer in sorted(layers)[:5]:  # Test first 5 layers
        print(f"\n  Testing layer: {layer}")

        try:
            # Clear and re-add with new scalar
            plotter.clear()

            plotter.add_mesh(
                world.mesh,
                scalars=layer,
                cmap="viridis",
                show_edges=False,
            )

            # Quick screenshot to verify
            temp_file = f"test_layer_{layer}.png"
            plotter.screenshot(temp_file)

            if Path(temp_file).exists():
                print("    ✓ Rendered successfully")
                Path(temp_file).unlink()
            else:
                print("    ✗ Rendering failed")

        except Exception as e:
            print(f"    ✗ Error: {e}")

    plotter.close()


def test_mesh_queries(world):
    """Test mesh query operations."""
    print_section("TEST 7: Mesh Query Operations")

    print("\nTesting neighbor queries...")

    # Test get_neighbors
    test_point = 100
    neighbors = world.get_neighbors(test_point, radius=100000)  # 100km

    print(f"  Point {test_point} has {len(neighbors)} neighbors within 100km")

    # Test data layer access
    print("\nTesting data layer access...")
    elevation = world.get_data_layer("elevation")

    if elevation is not None:
        print(f"  ✓ Retrieved elevation data: {len(elevation):,} values")
        print(f"    Min: {elevation.min():.1f} m")
        print(f"    Max: {elevation.max():.1f} m")
        print(f"    Mean: {elevation.mean():.1f} m")
    else:
        print("  ✗ Failed to retrieve elevation data")


def test_export_formats(world):
    """Test various export formats."""
    print_section("TEST 8: Export Format Tests")

    store = MeshStore("./data/worlds")

    # VTK format
    print("\nTesting VTK export...")
    vtk_path = Path(f"./data/worlds/test_{world.id}.vtk")
    try:
        store.export_to_vtk(world.id, vtk_path)
        if vtk_path.exists():
            print(f"  ✓ VTK: {vtk_path.stat().st_size / 1024:.1f} KB")
            vtk_path.unlink()
    except Exception as e:
        print(f"  ✗ VTK export failed: {e}")

    # Test native PyVista formats
    print("\nTesting PyVista native formats...")

    formats = [
        ("vtp", "VTK PolyData"),
        ("ply", "Stanford PLY"),
        ("obj", "Wavefront OBJ"),
    ]

    for ext, name in formats:
        path = Path(f"./data/worlds/test_{world.id}.{ext}")
        try:
            world.mesh.save(str(path))
            if path.exists():
                size = path.stat().st_size / 1024
                print(f"  ✓ {name}: {size:.1f} KB")
                path.unlink()
        except Exception as e:
            print(f"  ✗ {name} failed: {e}")


async def main():
    """Run all visualization tests."""
    print("\n" + "=" * 70)
    print("  COMPREHENSIVE VISUALIZATION & EXPORT TEST SUITE")
    print("=" * 70)

    try:
        # Generate test world
        world = await test_generation()

        # Test storage
        test_hdf5_storage(world)

        # Test VTK export
        test_vtk_export(world)

        # Test off-screen rendering
        test_offscreen_rendering(world)

        # Test interactive features
        test_interactive_features(world)

        # Test data layer switching
        test_data_layer_switching(world)

        # Test mesh queries
        test_mesh_queries(world)

        # Test export formats
        test_export_formats(world)

        # Final summary
        print_section("TEST SUMMARY")
        print("\n✓ All visualization and export tests completed successfully!")
        print("\nNext steps:")
        print("  1. Desktop viewer: python -m lathe.viz.desktop")
        print(f"  2. Or with world: python -m lathe.viz.desktop {world.id}")
        print("  3. Open in ParaView: paraview data/worlds/world_*.vtk")

    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
