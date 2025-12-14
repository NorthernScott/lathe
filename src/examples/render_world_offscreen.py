"""Render worlds off-screen (no display required)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pyvista as pv
from uuid import UUID
from lathe.storage.mesh_store import MeshStore


def main():
    """Render all worlds to images."""
    store = MeshStore()
    worlds = store.list_worlds()

    if not worlds:
        print("No worlds found. Generate one first with examples/test_tectonics.py")
        return

    print(f"Found {len(worlds)} world(s)")
    print()

    # Configure off-screen rendering
    pv.OFF_SCREEN = True

    for world_info in worlds:
        world_id = world_info["world_id"]
        name = world_info["name"]

        print(f"Rendering: {name}")

        # Load world
        world = store.load_world(UUID(world_id))

        # Get available data layers
        layers = world.list_data_layers()
        print(f"  Layers: {', '.join(layers)}")

        # Render each interesting layer
        for layer in ["elevation", "plate_id", "plate_boundary", "boundary_type"]:
            if layer not in layers:
                continue

            # Create plotter
            plotter = pv.Plotter(off_screen=True, window_size=(1600, 1200))
            plotter.set_background("black")

            # Choose colormap
            if layer == "elevation":
                cmap = "terrain"
            elif layer == "plate_id":
                cmap = "Accent"
            elif layer == "plate_boundary":
                cmap = "binary"
            elif layer == "boundary_type":
                cmap = "Set1"
            else:
                cmap = "viridis"

            # Add mesh
            plotter.add_mesh(
                world.mesh,
                scalars=layer,
                cmap=cmap,
                show_edges=False,
                smooth_shading=True,
                scalar_bar_args={
                    "title": layer.replace("_", " ").title(),
                    "vertical": True,
                    "height": 0.75,
                },
            )

            # Set camera
            radius = world.params.radius
            plotter.camera_position = [
                (radius * 2.5, radius * 2.5, radius * 2.5),
                (0, 0, 0),
                (0, 0, 1),
            ]

            # Save screenshot
            output_dir = Path("renders")
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / f"{world_id}_{layer}.png"
            plotter.screenshot(str(output_file))
            plotter.close()

            print(f"    ✓ {output_file.name}")

    print()
    print(f"✓ Rendered {len(worlds)} world(s) to ./renders/")
    print()


if __name__ == "__main__":
    main()
