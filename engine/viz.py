import cmocean as cmo  # noqa: F401 Used via PyVista.
import pyvista as pv

from engine.world import World


class Visualizer:
    def __init__(self, world: World) -> None:
        self.world: World = world
        self.dataset_names: list[str] = []

        if hasattr(self.world.mesh, "point_data") and self.world.mesh.point_data:
            for key in self.world.mesh.point_data.keys():
                self.dataset_names.append(key)

            print(self.dataset_names)

        # Store the original mesh points and normals.
        self.original_points = self.world.mesh.points.copy()
        self.original_surface_normals = self.world.mesh.compute_normals(
            cell_normals=True, point_normals=True, inplace=True
        )

        # Smooth the mesh.
        pv.PolyDataFilters.smooth_taubin(self.world.mesh)  # Defaults to 20 passes with a pass band of 0.1.

    def __str__(self) -> str:
        return f"Visualizer(name={self.world.name}, radius={self.world.radius}, zscale={self.world.zscale})"

    def __repr__(self) -> str:
        return f"Visualizer(name={self.world.name!r}, radius={self.world.radius!r}, zscale={self.world.zscale!r})"

    def viz(self) -> None:
        """
        Use PyVista to visualize the terrain mesh.

        Args:
            mesh (type[pv.PolyData]): The terrain mesh to visualize.
            radius (int): The radius of the world.
            zscale (int): The scale factor by which to exaggerate the terrain.
            zmin (int): The minimum scaled elevation value.
            zmax (int): The maximum scaled elevation value.
            scalars (type[pv.PolyData.point_data]): An array of scalar values used to color the mesh.
            name (str): The name of the world.

        Returns:
        None: Returns nothing.
        """

        # Configure global render options.
        pv.plotter._ALL_PLOTTERS.clear()
        pv.set_plot_theme("dark")
        pv.global_theme.lighting = True

        # Create and configure plotter.
        plotter = pv.Plotter(
            notebook=False,
        )
        plotter.enable_anti_aliasing(aa_type="ssaa", all_renderers=True)
        plotter.enable_hidden_line_removal(all_renderers=True)
        plotter.camera.zoom(0.75)
        pv.Plotter.enable_terrain_style(plotter, mouse_wheel_zooms=True)
        plotter.renderer
        plotter.iren.initialize()

        # Define scalars.
        scalars = self.world.mesh.point_data["Elevations"]

        # Create dictionary of parameters to control the scalar bar.
        scalar_args = {
            "interactive": False,
            "height": 0.25,
            "vertical": True,
            "position_x": 0.05,
            "position_y": 0.05,
            "title_font_size": 20,
            "label_font_size": 16,
            "shadow": True,
            "n_labels": 7,
            "italic": False,
            "fmt": "%.1f",
            "font_family": "courier",
        }

        # Create dictionary of annotations.
        annotations: dict = {}

        # Compute surface normals and apply global scale to z-axis, to exaggerate the terrain.
        self.world.mesh.warp_by_scalar(scalars="Elevations", factor=self.world.zscale, inplace=True, progress_bar=False)
        self.world.mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)

        # Add the mesh to the plotter with the initial scalar dataset
        plotter.add_mesh(
            self.world.mesh,
            name=self.world.name,
            scalars=scalars,
            scalar_bar_args=scalar_args,
            annotations=annotations,
            style="surface",
            smooth_shading=True,
            show_edges=False,
            edge_color="red",
            line_width=1,
            cmap="cmo.topo",
            lighting=True,
            pickable=False,
            preference="cell",
        )

        # HACK: Mesh isovalues allow me to essentially draw 3D contour lines based on a given scalar, which could be elevations, temperature, precipitation, tectonic plates, etc.
        # plotter.add_mesh_isovalue(
        #     self.world.mesh,
        #     scalars="Elevations",
        #     compute_normals=True,
        #     compute_gradients=True,
        #     compute_scalars=True,
        #     preference="point",
        #     title="Z-Scale",
        #     pointa=(0.4, 0.9),
        #     pointb=(0.9, 0.9),
        #     widget_color=None,
        # )

        # Add elevation scale slider and define callback function.
        def update_zscale(value) -> None:
            self.world.mesh.points = self.original_points
            self.world.mesh.warp_by_scalar(scalars="Elevations", factor=value, inplace=True, progress_bar=False)
            self.world.mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)

        plotter.add_slider_widget(
            update_zscale,
            rng=(1, 40),
            value=self.world.zscale,
            title="Elevation Scale Factor",
            pointa=(0.75, 0.90),
            pointb=(0.95, 0.90),
            pass_widget=False,
            interaction_event="always",
            style="modern",
        )

        # Set the camera position
        plotter.camera_position = [
            (self.world.radius * 2, self.world.radius * 2, self.world.radius * 2),  # Position
            (0, 0, 0),  # Focal point
            (0, 0, 1),  # View up direction
        ]

        # Display the plotter.
        plotter.render()
        plotter.show()
