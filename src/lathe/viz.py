# -*- coding: utf-8 -*-

# import core libraries.
import logging

# import third-party modules.
import pyvista as pv


def viz(
    mesh: type[pv.PolyData],
    radius: int,
    zscale: int,
    zmin: int,
    zmax: int,
    scalars: type[pv.PolyData.point_data],
    name: str,
) -> None:
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
    pv.global_theme.cmap = "topo"
    pv.global_theme.lighting = False

    # Instatiate the plotter object.

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

    ocean_shell = pv.ParametricEllipsoid(radius, radius, radius, u_res=300, v_res=300)

    pl.add_mesh(
        ocean_shell,
        show_edges=False,
        smooth_shading=True,
        color="blue",
        opacity=0.15,
    )

    pl.camera.zoom(1.25)
    pl.enable_terrain_style(mouse_wheel_zooms=True)

    logging.info("Plot output.")

    pl.render()
    pl.show()

    return None