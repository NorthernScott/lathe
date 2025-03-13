import cmocean as cmo  # type: ignore  # noqa: F401
import pyvista as pv
import pyvistaqt as pvqt
from numpy import array

from engine.world import World


class Visualizer:
    def __init__(self, world: World) -> None:
        """Initialize the object and render the world."""
        # self.world: World = world
        self.dataset_names: list[str] = []

        # Store the original mesh points.
        # self.original_points: pyvista_ndarray = self.world.mesh.points.copy()

        # Configure global plotter options.
        pv.set_plot_theme("dark")  # type: ignore
        pv.global_theme.lighting = True

        # Instantiate and configure plotter.
        plotter = pvqt.BackgroundPlotter(  # type: ignore
            notebook=False,
            shape=(1, 1),
            border=True,
            border_color="white",
            window_size=(1080, 720),
            polygon_smoothing=True,
            lighting="light kit",
        )
        # Clear plotter.
        plotter.clear()  # type: ignore

        # Deep clean plotter memory buffer.
        plotter.deep_clean()

        # plotter.enable_hidden_line_removal(all_renderers=True)  # type: ignore
        # plotter.camera.zoom(0.75)  # type: ignore
        # pv.Plotter.enable_terrain_style(plotter, mouse_wheel_zooms=True)  # type: ignore

        # Create dictionary of parameters to control the scalar bar.
        scalar_args: dict[str, bool | float | int | str] = {
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
        annotations: dict[str, str] = {}

        # Set default scalars.
        world.mesh.set_active_scalars(name="Elevations")  # type: ignore
        # scalars: pyvista_ndarray = self.world.mesh.point_data["Elevations"]

        # Create a list of scalars.
        if hasattr(world.mesh, "point_data") and world.mesh.point_data:
            for key in world.mesh.point_data.keys():
                self.dataset_names.append(key)

            print(self.dataset_names)

        # Add the base topographical mesh to an actor.
        plotter.add_mesh(  # type: ignore
            world.mesh,
            name=world.name,
            # scalars=scalars,
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

        # Add axes.
        plotter.add_lines(  # type: ignore
            lines=array(
                [
                    [-world.radius * 2, 0, 0],
                    [world.radius * 2, 0, 0],
                    [0, -world.radius * 2, 0],
                    [0, world.radius * 2, 0],
                    [0, 0, -world.radius * 2],
                    [0, 0, world.radius * 2],
                ],
            ),
            color="red",
        )

        # Define a callback function for the dropdown widget.

        def change_scalar_dataset(value: bool) -> None:
            if value is True | False:
                current_scalar_name: str = world.mesh.active_scalars_name
                try:
                    if current_scalar_name in self.dataset_names:
                        current: int = self.dataset_names.index(current_scalar_name)
                        new: str = self.dataset_names[(current + 1) % len(self.dataset_names)]
                        world.mesh.set_active_scalars(name=new)  # type: ignore
                    else:
                        raise ValueError
                except ValueError:
                    print(f"Warning: Active scalar '{current_scalar_name}' is not in the dataset names list.")

        # Add checkbox widget to select scalars.
        plotter.add_text("Change Scalars:", position="upper_left", font_size=12)  # type: ignore

        plotter.add_checkbox_button_widget(  # type: ignore
            change_scalar_dataset,
            value=False,
            position=(10.0, 10.0),
            size=50,
            border_size=5,
            color_on="blue",
            color_off="grey",
            background_color="white",
        )

        # HACK: Mesh isovalues allow me to essentially draw 3D contour lines based on a given scalar, which could be elevations, temperature, precipitation, tectonic plates, etc.
        # Add elevation contours isovalue slider.
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

        # HACK: The elevation scale slider works well but with higher mesh resolution exceeds what my graphics card can handle. The effect is interesting but not necessary, and ultimately a fixed z-scale value works well to give some texture.
        # Add elevation scale slider and define callback function.
        # def update_zscale(value) -> None:
        #     self.world.mesh.points = self.original_points
        #     self.world.mesh.warp_by_scalar(scalars="Elevations", factor=value, inplace=True, progress_bar=False)
        #     self.world.mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)

        # plotter.add_slider_widget(
        #     update_zscale,
        #     rng=(1, 40),
        #     value=self.world.zscale,
        #     title="Elevation Scale Factor",
        #     pointa=(0.75, 0.90),
        #     pointb=(0.95, 0.90),
        #     pass_widget=False,
        #     interaction_event="always",
        #     style="modern",
        # )

        # Set the camera position
        # plotter.camera_position = [
        #     (world.radius * 2, world.radius * 2, world.radius * 2),  # Position
        #     (0, 0, 0),  # Focal point
        #     (0, 0, 1),  # View up direction
        # ]

        # Display the plotter.
        plotter.render()  # type: ignore
        plotter.show()  # type: ignore
        plotter.app.exec_()
