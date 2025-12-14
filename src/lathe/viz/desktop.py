"""Desktop visualization using PyVista and Qt."""

import sys
from pathlib import Path
from uuid import UUID

from pyvistaqt import QtInteractor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lathe.storage.mesh_store import MeshStore


class WorldViewer(QMainWindow):
    """Desktop viewer for generated worlds."""

    def __init__(self, world_id: UUID | None = None):
        """Initialize the world viewer.

        Args:
            world_id: UUID of world to load (None to show file picker)
        """
        super().__init__()

        self.world_id = world_id
        self.world = None
        self.mesh_store = MeshStore("./data/worlds")
        self.current_scalar = "elevation"

        self.setWindowTitle("Lathe World Viewer")
        self.setGeometry(100, 100, 1400, 800)

        self._setup_ui()

        if world_id:
            self.load_world(world_id)

    def _setup_ui(self):
        """Set up the user interface."""
        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Create main layout
        main_layout = QVBoxLayout(central)

        # Create top control bar
        control_bar = self._create_control_bar()
        main_layout.addWidget(control_bar)

        # Create splitter for 3D view and info panel
        splitter = QSplitter(Qt.Horizontal)

        # Left: PyVista 3D viewer
        # Create QtInteractor with explicit parent to avoid X11 window issues
        self.plotter_widget = QtInteractor(parent=splitter)
        self.plotter = self.plotter_widget
        splitter.addWidget(self.plotter_widget)

        # Right: Info panel
        info_panel = self._create_info_panel()
        splitter.addWidget(info_panel)

        # Set splitter sizes (70% 3D view, 30% info)
        splitter.setSizes([1000, 400])

        main_layout.addWidget(splitter)

        # Configure PyVista plotter
        self.plotter.set_background("black")
        self.plotter.add_text("Load a world to begin", position="upper_left", font_size=12)

        # Now that plotter is created, populate the world list
        self._refresh_world_list()

    def _create_control_bar(self) -> QWidget:
        """Create the control bar with buttons and selectors."""
        control_widget = QWidget()
        layout = QHBoxLayout(control_widget)

        # World selector
        layout.addWidget(QLabel("World:"))
        self.world_combo = QComboBox()
        self.world_combo.currentTextChanged.connect(self._on_world_selected)
        layout.addWidget(self.world_combo)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_world_list)
        layout.addWidget(refresh_btn)

        # Scalar selector
        layout.addWidget(QLabel("   Data Layer:"))
        self.scalar_combo = QComboBox()
        self.scalar_combo.currentTextChanged.connect(self._on_scalar_changed)
        layout.addWidget(self.scalar_combo)

        # Reset camera button
        reset_btn = QPushButton("Reset Camera")
        reset_btn.clicked.connect(self._reset_camera)
        layout.addWidget(reset_btn)

        layout.addStretch()

        # Don't refresh list here - will be done after plotter is created

        return control_widget

    def _create_info_panel(self) -> QWidget:
        """Create the information panel."""
        info_widget = QWidget()
        layout = QVBoxLayout(info_widget)

        layout.addWidget(QLabel("<h3>World Information</h3>"))

        self.info_browser = QTextBrowser()
        self.info_browser.setOpenExternalLinks(False)
        layout.addWidget(self.info_browser)

        return info_widget

    def _refresh_world_list(self):
        """Refresh the list of available worlds."""
        self.world_combo.clear()

        worlds = self.mesh_store.list_worlds()

        for world in worlds:
            display_name = f"{world['name']} ({world['num_points']:,} pts)"
            self.world_combo.addItem(display_name, world["world_id"])

        # If we have a world_id, select it
        if self.world_id:
            for i in range(self.world_combo.count()):
                if self.world_combo.itemData(i) == str(self.world_id):
                    self.world_combo.setCurrentIndex(i)
                    break

    def _on_world_selected(self, text: str):
        """Handle world selection."""
        if not text or not hasattr(self, 'plotter'):
            return

        world_id = self.world_combo.currentData()
        if world_id:
            self.load_world(UUID(world_id))

    def _on_scalar_changed(self, scalar_name: str):
        """Handle scalar selection change."""
        if not scalar_name or not self.world or not hasattr(self, 'plotter'):
            return

        self.current_scalar = scalar_name
        self._update_mesh_scalars()

    def load_world(self, world_id: UUID):
        """Load and display a world.

        Args:
            world_id: UUID of world to load
        """
        try:
            # Load world
            self.world = self.mesh_store.load_world(world_id)
            self.world_id = world_id

            # Update scalar selector
            self.scalar_combo.clear()
            self.scalar_combo.addItems(self.world.list_data_layers())

            # Set default scalar
            if self.world.has_data_layer("elevation"):
                self.current_scalar = "elevation"
                self.scalar_combo.setCurrentText("elevation")
            else:
                self.current_scalar = self.world.list_data_layers()[0]

            # Display mesh
            self._display_mesh()

            # Update info panel
            self._update_info_panel()

        except Exception as e:
            self.plotter.add_text(
                f"Error loading world: {e}",
                position="upper_left",
                font_size=12,
                color="red",
            )

    def _display_mesh(self):
        """Display the mesh in the 3D viewer."""
        if not self.world:
            return

        # Clear previous mesh
        self.plotter.clear()

        # Add mesh
        self.plotter.add_mesh(
            self.world.mesh,
            scalars=self.current_scalar,
            cmap="terrain" if self.current_scalar == "elevation" else "viridis",
            show_edges=False,
            smooth_shading=True,
            scalar_bar_args={
                "title": self.current_scalar.replace("_", " ").title(),
                "height": 0.75,
                "vertical": True,
                "position_x": 0.05,
                "position_y": 0.125,
            },
        )

        # Add axes
        import numpy as np

        radius = self.world.params.radius

        # X axis (red)
        self.plotter.add_lines(
            np.array([[-radius * 1.5, 0, 0], [radius * 1.5, 0, 0]]),
            color="red",
            width=2,
        )
        # Y axis (green)
        self.plotter.add_lines(
            np.array([[0, -radius * 1.5, 0], [0, radius * 1.5, 0]]),
            color="green",
            width=2,
        )
        # Z axis (blue)
        self.plotter.add_lines(
            np.array([[0, 0, -radius * 1.5], [0, 0, radius * 1.5]]),
            color="blue",
            width=2,
        )

        # Reset camera
        self._reset_camera()

    def _update_mesh_scalars(self):
        """Update the displayed scalar data."""
        if not self.world:
            return

        # Update active scalars
        self.world.mesh.set_active_scalars(self.current_scalar)

        # Redisplay
        self._display_mesh()

    def _reset_camera(self):
        """Reset camera to default position."""
        if not self.world or not hasattr(self, 'plotter'):
            return

        radius = self.world.params.radius

        self.plotter.camera_position = [
            (radius * 2, radius * 2, radius * 2),  # Position
            (0, 0, 0),  # Focal point
            (0, 0, 1),  # View up
        ]

    def _update_info_panel(self):
        """Update the information panel with world details."""
        if not self.world:
            self.info_browser.setHtml("<p>No world loaded</p>")
            return

        # Get statistics
        elevation = self.world.get_data_layer("elevation")
        landforms = self.world.get_data_layer("landforms")

        html = f"""
        <h3>{self.world.params.name}</h3>

        <p><b>World ID:</b><br/>{self.world.id}</p>

        <h4>Mesh Information</h4>
        <table>
        <tr><td><b>Points:</b></td><td>{self.world.num_points:,}</td></tr>
        <tr><td><b>Faces:</b></td><td>{self.world.num_faces:,}</td></tr>
        <tr><td><b>Recursion:</b></td><td>{self.world.params.recursion}</td></tr>
        <tr><td><b>Radius:</b></td><td>{self.world.params.radius:,} m</td></tr>
        </table>

        <h4>Parameters</h4>
        <table>
        <tr><td><b>Seed:</b></td><td>{self.world.params.seed}</td></tr>
        <tr><td><b>Ocean %:</b></td><td>{self.world.params.ocean_percent * 100:.0f}%</td></tr>
        <tr><td><b>Elevation Range:</b></td><td>{self.world.params.zmin} to {self.world.params.zmax} m</td></tr>
        </table>
        """

        if elevation is not None:
            html += f"""
            <h4>Elevation Statistics</h4>
            <table>
            <tr><td><b>Minimum:</b></td><td>{elevation.min():.1f} m</td></tr>
            <tr><td><b>Maximum:</b></td><td>{elevation.max():.1f} m</td></tr>
            <tr><td><b>Mean:</b></td><td>{elevation.mean():.1f} m</td></tr>
            <tr><td><b>Std Dev:</b></td><td>{elevation.std():.1f} m</td></tr>
            </table>
            """

        if landforms is not None:
            land_pct = (landforms.sum() / len(landforms)) * 100
            html += f"""
            <h4>Land Distribution</h4>
            <table>
            <tr><td><b>Land:</b></td><td>{land_pct:.1f}%</td></tr>
            <tr><td><b>Ocean:</b></td><td>{100 - land_pct:.1f}%</td></tr>
            </table>
            """

        # Data layers
        html += f"""
        <h4>Data Layers ({len(self.world.list_data_layers())})</h4>
        <ul>
        """
        for layer in sorted(self.world.list_data_layers()):
            html += f"<li>{layer}</li>"
        html += "</ul>"

        # Metadata
        if self.world.metadata.get("generation_complete"):
            gen_time = self.world.metadata.get("generation_time_seconds", 0)
            pipeline = self.world.metadata.get("pipeline_steps", [])

            html += f"""
            <h4>Generation Info</h4>
            <table>
            <tr><td><b>Time:</b></td><td>{gen_time:.2f} seconds</td></tr>
            <tr><td><b>Pipeline:</b></td><td>{' → '.join(pipeline)}</td></tr>
            </table>
            """

        self.info_browser.setHtml(html)


def main():
    """Main entry point for desktop viewer."""
    import argparse

    parser = argparse.ArgumentParser(description="Lathe Desktop World Viewer")
    parser.add_argument("world_id", nargs="?", help="UUID of world to load")
    args = parser.parse_args()

    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show viewer
    world_id = UUID(args.world_id) if args.world_id else None
    viewer = WorldViewer(world_id)
    viewer.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
