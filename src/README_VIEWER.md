# Lathe Desktop Viewer

Interactive 3D viewer for exploring generated worlds.

## Quick Start

```bash
./launch_viewer.sh
```

## Features

- **3D Interactive View** - Rotate, zoom, pan the world
- **Layer Switching** - View elevation, plates, boundaries, etc.
- **World Browser** - Load any generated world
- **Info Panel** - View world statistics and metadata
- **Camera Controls** - Reset view, adjust perspective

## Requirements

- Display server (X11 or Wayland with XWayland)
- Qt6 and PyVista installed

## Usage

### Launch the Viewer

```bash
./launch_viewer.sh
```

### Load a Specific World

```bash
./launch_viewer.sh <world-uuid>
```

### Controls

- **Left click + drag** - Rotate
- **Right click + drag** - Pan
- **Scroll wheel** - Zoom
- **Reset Camera button** - Reset view

### Viewing Different Layers

Use the "Data Layer" dropdown to switch between:
- **elevation** - Terrain height (terrain colormap)
- **plate_id** - Tectonic plates (color-coded)
- **plate_boundary** - Plate boundaries (binary)
- **boundary_type** - Convergent/divergent/transform
- **landforms** - Land vs ocean mask

## Troubleshooting

### "X Error: BadWindow"

If you see this error, you're on Wayland and need to use the launcher script:
```bash
./launch_viewer.sh  # ✓ Works
python -m lathe.viz.desktop  # ✗ Doesn't work on Wayland
```

The launcher sets `QT_QPA_PLATFORM=xcb` which forces Qt to use X11 compatibility mode.

### Alternative: Set Environment Variable

```bash
export QT_QPA_PLATFORM=xcb
python -m lathe.viz.desktop  # Now works
```

### No Worlds Available

Generate a world first:
```bash
python examples/test_tectonics.py
```

Then launch the viewer and select it from the dropdown.

## Off-Screen Rendering (Headless)

If you don't have a display or want to generate images:
```bash
python examples/render_world_offscreen.py
```

This creates PNG images in `renders/` directory.
