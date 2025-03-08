# import cmocean as cmo  # noqa: F401 Used via PyVista.
import pyvista as pv
# import numpy as np

from engine.world import World


class Visualizer:
    def __init__(
        self,
        world: World,
        name: str,
        radius: int,
        zscale: int,
    ) -> None:
        self.world: World = world
        self.world_name: str = world.name
        self.world_radius: int = world.radius
        self.world_zscale: int = world.zscale
        self.dataset_names: list = world.mesh.array_names

        if hasattr(self.world.mesh, "point_data") and self.world.mesh.point_data:
            for key in self.world.mesh.point_data.keys():
                self.dataset_names.append(self.world.mesh.point_data[key])

    def __str__(self) -> str:
        return f"Visualizer(name={self.world_name}, radius={self.world_radius}, zscale={self.world_zscale})"

    def __repr__(self) -> str:
        return f"Visualizer(name={self.world_name!r}, radius={self.world_radius!r}, zscale={self.world_zscale!r})"

    def viz(self) -> None:
        """
        Use PyVista to visualize the terrain mesh..

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

        # Set up the PyVista plotter.
        pv.plotter._ALL_PLOTTERS.clear()

        pv.set_plot_theme("dark")
        pv.global_theme.anti_aliasing = "ssaa"
        pv.global_theme.lighting = True

        # Instatiate the plotter object.

        # Create a plotter object
        plotter = pv.Plotter()

        # Function to update the scalar dataset
        def update_scalars(self, value) -> None:
            scalar_name = self.dataset_names[int(value)]
            plotter.update_scalars(self.world.mesh.point_data[scalar_name], render=True)

        # Add the mesh to the plotter with the initial scalar dataset
        plotter.add_mesh(
            self.world.mesh, scalars=self.dataset_names[0], scalar_bar_args={"title": self.dataset_names[0]}
        )

        # Add a slider widget to switch between scalar datasets
        plotter.add_slider_widget(
            update_scalars,
            rng=[0, len(self.dataset_names) - 1],
            title="Scalar Dataset",
            value=0,
            interaction_event="always",
            style="modern",
            pointa=(0.025, 0.1),
            pointb=(0.225, 0.1),
        )

        # Show the plotter
        plotter.show()

        """
        pl = pv.Plotter(notebook=False)
        pl.enable_anti_aliasing()
        pl.enable_hidden_line_removal(all_renderers=True)

        # Create dictionary of parameters to control the scalar bar.

        scalar_args = dict(
            interactive=False,
            height=0.25,
            vertical=True,
            position_x=0.05,
            position_y=0.05,
            title_font_size=20,
            label_font_size=16,
            shadow=True,
            n_labels=7,
            italic=False,
            fmt="%.1f",
            font_family="courier",
        )
        annotations = {}

        # world_mesh.compute_normals(cell_normals=True, point_normals=True, inplace=True)

        # Apply global scale factor to the mesh, to exaggerate the terrain.

        mesh = mesh.warp_by_scalar(factor=-zscale, inplace=False)

        # Add the world mesh to the plotter.

        pl.add_mesh(
            mesh,
            name=name,
            scalars=scalars,
            scalar_bar_args=scalar_args,
            show_scalar_bar=True,
            annotations=annotations,
            style="surface",
            smooth_shading=True,
            show_edges=False,
            edge_color="red",
            line_width=1,
            cmap="cmo.topo",
            lighting=True,
            pickable=True,
            preference="cell",
        )

        # NOTE: The ocean shell is not currently used in the visualization. Seems to just wash out the colours of the terrain and isn't very useful.
        # Add the ocean shell to the plotter.
        # ocean_shell = pv.ParametricEllipsoid(radius, radius, radius, u_res=300, v_res=300)


        pl.camera.zoom(1.25)
        pl.enable_terrain_style(mouse_wheel_zooms=True)

        pl.render()
        pl.show()

        return None
        """
