# -*- coding: utf-8 -*-

# import core modules
import logging

# import external dependencies
import pyvista as pv

# import pyvistaqt as pvqt


def viz(world_mesh, scalars, radius, zscale, zmin, zmax):
    logging.debug(msg="Starting viz().")

    logging.debug(msg="Setup PyVista plotter.")

    pv.plotter._ALL_PLOTTERS.clear()

    pv.set_plot_theme("dark")
    pv.global_theme.anti_aliasing = "ssaa"
    pv.global_theme.cmap = "topo"
    pv.global_theme.lighting = False

    # colour_map = "terrain"

    logging.debug(msg="Instantiate plotter.")
    pl = pv.Plotter(notebook=False)
    # pl = pvqt.BackgroundPlotter(notebook=False)
    pl.enable_anti_aliasing()
    pl.enable_hidden_line_removal(all_renderers=True)

    logging.debug(msg="Create dictionary of parameters to control the scalar bar.")

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

    world_mesh.compute_normals(cell_normals=True, point_normals=True, inplace=True)
    globe_mesh = world_mesh.warp_by_scalar(factor=-50)

    pl.add_mesh(
        globe_mesh,
        name="Base Terrain",
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

    # ocean_shell = pv.ParametricEllipsoid(radius, radius, radius, u_res=300, v_res=300)

    # pl.add_mesh(
    #     ocean_shell,
    #     show_edges=False,
    #     smooth_shading=True,
    #     color="blue",
    #     opacity=0.15,
    # )

    pl.show_bounds(
        grid=True,
        location="back",
        axes_ranges=[0, 6400, 0, 6400, 0, 6400],
        show_zlabels=True,
    )

    pl.camera.zoom(1.25)
    pl.enable_terrain_style(mouse_wheel_zooms=True)

    logging.info("Plot output.")

    # pl.export_html('pv.html')

    # pl.app.exec_()
    pl.render()
    pl.show()
