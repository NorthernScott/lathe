import json
import logging
import random
import time
from io import TextIOWrapper
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import numpy as np
import pyvista as pv
import typer
from mylogger import err_con, std_con
from rich.logging import RichHandler
from rich.table import Table
from terrain import sample_octaves
from util import Mesh, MeshArray, create_mesh, now, rescale, save_world, xyz2latlon
from viz import viz

if TYPE_CHECKING:
    from numpy.typing import NDArray

# Define global defaults.
RADIUS: int = 6378100  # Radius of the world in meters.
ZMIN: int = round(
    number=-(RADIUS * 0.0015),
)  # The lowest elevation in the world, in meters.
ZMAX: int = round(
    number=RADIUS * 0.0015,
)  # The highest elevation in the world, in meters.
ZRANGE: float = ZMAX - ZMIN
ZTILT: float = 23.4  # Used in mapping spherical coordinates to lat-lon coordinates.
ZSCALE: int = 20  # A scaling factor for elevations to make them visible in the plot.
OCEAN_PERCENT: float = 0.55  # Sets the point of elevation 0 relative to the ZRANGE.
OCEAN_POINT: float = OCEAN_PERCENT * ZRANGE
RECURSION: int = 9  # The level of detail in the mesh. Values above 9 may be slow to render.
OCTAVES: int = 8  # Sets the number of iterations to use for noise sampling.
LOGLEVEL: str = "WARNING"
LOGFORMAT: str = "\r\n%(message)s"
INIT_ROUGHNESS: float = 1.5  # Sets the initial roughness (frequency) of the first octave of noise.
INIT_STRENGTH: float = 0.4  # Sets the initial strength (amplitude) of the first octave of noise.
ROUGHNESS: float = 2.5  # Multiply roughness by this much per octave.
PERSISTENCE: float = 0.5  # Multiply strength by this much per octave.
PLATESNUM: int = round(
    number=RADIUS / 500_000,
)  # The number of tectonic plates to generate.

SEED_MIN = 1  # Seed must be a positive integer between 1 and 255.
SEED_MAX = 255  # Seed must be a positive integer between 1 and 255.


# Setup functions.
def getPlanetName() -> str:
    """Return a random planet name from planetnames.json."""
    file_path = Path(Path(__file__).parent, "planetnames.json")
    with TextIOWrapper, Path.open(file=file_path) as f:
        data = json.load(fp=f)
        names = data["planetNames"]

    return random.choice(seq=names)


# Main thread.
def main(  # noqa: PLR0913, PLR0915
    name: Annotated[
        str,
        typer.Argument(
            default_factory=getPlanetName,
            help="A name for the world. If not provided, a random name is chosen.",
        ),
    ],
    save: Annotated[
        bool,
        typer.Option(
            help="Sets whether the mesh and world data are saved to output files.",
        ),
    ] = False,
    visualize: Annotated[
        bool,
        typer.Option(
            help="Sets whether the world is visualized in a 3D plot.",
        ),
    ] = True,
    seed: Annotated[
        int,
        typer.Option(help="The world seed to be used. Defaults to a random integer."),
    ] = 0,
    radius: Annotated[
        int,
        typer.Option(
            help="The radius of the world in meters. (Earth ~= 6378100 m.)",
        ),
    ] = RADIUS,
    recursion: Annotated[
        int,
        typer.Option(
            help="The detail level of the mesh. More than 9 may cause slow rendering.",
        ),
    ] = RECURSION,
    ztilt: Annotated[
        float,
        typer.Option(
            help="Controls the z-axis tilt of the planet.",
        ),
    ] = ZTILT,
    zmin: Annotated[
        int,
        typer.Option(
            help="The lowest elevation value on the planet.",
        ),
    ] = ZMIN,
    zmax: Annotated[
        int,
        typer.Option(
            help="The highest elevation value on the planet.",
        ),
    ] = ZMAX,
    ocean_percent: Annotated[
        float,
        typer.Option(
            help="Sets the global sea level relative to the elevation range.",
        ),
    ] = OCEAN_PERCENT,
    scale: Annotated[
        int,
        typer.Option(
            help="Sets a scale factor for elevations to make them visible in the plot.",
        ),
    ] = ZSCALE,
    octaves: Annotated[
        int,
        typer.Option(
            help="Sets the complexity of the generated noise.",
        ),
    ] = OCTAVES,
    loglevel: Annotated[
        str,
        typer.Option(help="Sets the verbosity of the logger."),
    ] = LOGLEVEL,
    platesnum: Annotated[  # noqa: ARG001
        int,
        typer.Option(
            help="Sets the number of tectonic plates to create. --Not in use.--",
        ),
    ] = PLATESNUM,
) -> None:
    """Generate a 3D mesh of a planet, apply elevations, and visualize the result.

    Args:
        name (str, optional): A name for the world.
        save (bool, optional): Whether to save world. Defaults to False.
        visualize (bool, optional): Whether to display the world. Defaults to True.
        seed (int, optional): The world seed to be used. Defaults to a random number.
        radius (int, optional): The radius of the world in meters.
        recursion (int, optional): The number of recursions used in creating the mesh.
        ztilt (float, optional): Controls the z-axis tilt of the planet.
        zmin (int, optional): The lowest elevation on the planet.
        zmax (int, optional): The highest elevation value on the planet.
        ocean_percent (float, optional): The global sea level relative to elevation.
        scale (int, optional): A multiplier to make elevations visible when displayed.
        octaves (int, optional): The number of octaves to use for noise sampling.
        loglevel (str, optional): The verbosity of the logger.
        platesnum (int, optional): The number of tectonic plates to create. -Not used.-

    Returns:
        None.

    """
    # Setup logger.

    logging.basicConfig(
        level=loglevel,
        format=LOGFORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )

    timer_start: float = time.perf_counter()

    # Set world seed and parameters.

    std_con.print("Setting world seed and parameters.\r\n")

    try:
        if seed != 0 and (seed < SEED_MIN or seed > SEED_MAX):
            world_seed = 0
            world_seed_string = "Random"
            std_con.print(f"Seed must be an integer between {SEED_MIN} and {SEED_MAX}. Setting to random seed.\r\n")
        else:
            world_seed = seed, world_seed_string = str(world_seed)
    except ValueError as e:
        err_con.print(f"Seed {e} is not an integer between {SEED_MIN} and {SEED_MAX}.\r\n")

    zrange: float = zmax - zmin

    ocean_point: float = ocean_percent * zrange

    # Create world_params dictionary.

    world_params = {
        "name": name,
        "timestamp": now(),
        "seed": world_seed_string,
        "radius": radius,
        "recursion": recursion,
        "octaves": octaves,
        "ztilt": ztilt,
        "zmin": zmin,
        "zmax": zmax,
        "zrange": zrange,
        "ocean_percent": ocean_percent,
        "ocean_point": ocean_point,
    }

    # Display world paramters.

    params_table = Table("Key", "Value")
    params_table.title = "World Parameters"
    params_table.title_style = "bold magenta"
    params_table.add_row("Name", name)
    params_table.add_row("Timestamp", str(now()))
    params_table.add_row("World Seed", world_seed_string)
    params_table.add_row("Radius", str(radius))
    params_table.add_row("Recursion Factor", str(recursion))
    params_table.add_row("Octaves (#)", str(octaves))
    params_table.add_row("Axial Tilt", str(ztilt))
    params_table.add_row("Lowest Elevation", str(zmin))
    params_table.add_row("Highest Elevation", str(zmax))
    params_table.add_row("Elevation Range", str(zrange))
    params_table.add_row("Ocean Percent", str(ocean_percent))
    params_table.add_row("Sea Level", str(ocean_point))
    params_table.add_row("Log Display", str(loglevel))

    std_con.print(params_table)

    # TODO @CNCBob: Determine how ocean_percent impacts surface area water cover. Ocean_percent essentially sets a surface water level for the display mask. I'm not sure it's actually necessary to set a water mask, since we assume that sea level = 0 m. Our rescale function handles this, and we should be able to change the map display accordingly. That said, a value to set the water level or % of surface covered by ocean would be helpful. I need to understand how this value relates to that. For reference, the percentage of the Earth's surface covered by water is approximately 71%.

    # Create world mesh, points arrays, and faces arrays.

    std_con.print("Creating world mesh.\r\n")

    world_mesh: Mesh = create_mesh(radius=radius, recursion=recursion)

    std_con.print(f"World Mesh:\r\n{world_mesh}\r\n")

    std_con.print(f"Sample of Points Array:\r\n{world_mesh.points}\r\n")

    std_con.print(f"Sample of Faces Array:\r\n{world_mesh.faces}\r\n")

    # Generate elevations.

    std_con.print("Generating elevations.\r\n")

    raw_elevations: MeshArray = sample_octaves(
        points=world_mesh.points,
        octaves=octaves,
        init_roughness=INIT_ROUGHNESS,
        init_strength=INIT_STRENGTH,
        roughness=ROUGHNESS,
        persistence=PERSISTENCE,
        radius=radius,
        seed=world_seed,
    )
    std_con.print(f"Sample of Raw Elevations:\r\n {raw_elevations} \r\n")

    # Generate elevation scalars.

    std_con.print("Applying elevations to mesh.\r\n")

    elevation_scalars: NDArray[np.float64] = ((raw_elevations) + radius) / radius

    std_con.print(f"Sample of Elevation Scalars:\r\n {elevation_scalars} \r\n")

    world_mesh.points[:, 0] *= elevation_scalars
    world_mesh.points[:, 1] *= elevation_scalars
    world_mesh.points[:, 2] *= elevation_scalars

    std_con.print(f"Sample of Modified Points Array:\r\n {world_mesh.points} \r\n")

    # Rescale elevations.

    std_con.print(f"Rescaling elevations within range {zmin} to {zmax}.\r\n")

    rescaled_elevations: NDArray[np.float64] = rescale(elevations=raw_elevations, zmin=zmin, zmax=zmax)

    std_con.print(f"Sample of Rescaled Elevations:\r\n {rescaled_elevations} \r\n")

    # Add rescaleq elevations to mesh as scalar dataset.

    std_con.print("Adding rescaled elevations to mesh as scalar dataset.\r\n")

    world_mesh.point_data["Elevations"] = rescaled_elevations

    std_con.print(f"Sample of Elevations Dataset:\r\n {world_mesh.point_data['Elevations']} \r\n")

    # Display world generation time.

    gen_timer_end: float = time.perf_counter()
    gen_timer: float = gen_timer_end - timer_start

    std_con.print(f"Terrain generated in {gen_timer:0.4f} seconds.\r\n")

    # HACK: Begin hackathon!

    # XYZ to Lat-Lon conversion.

    std_con.print("Converting XYZ to Lat-Lon coordinates.\r\n")

    lat, lon = xyz2latlon(mesh=world_mesh, radius=radius)

    latlon_timer_end: float = time.perf_counter()
    latlon_timer: float = latlon_timer_end - gen_timer_end

    std_con.print(f"Lat-Lon coordinates generated in {latlon_timer:0.4f} seconds.\r\n")

    # Create plate carree projection meshes.

    pc_x = lon * radius
    pc_y = lat * radius
    pc_z = rescaled_elevations
    pc_map = np.column_stack((pc_x, pc_y, pc_z))
    pc_mesh = pv.PolyData(pc_map)
    pc_mesh.delaunay_2d(inplace=True, progress_bar=True)
    pc_mesh.point_data["Elevations"] = rescaled_elevations
    pc_mesh.plot(
        show_edges=False,
        scalars="Elevations",
        cmap="topo",
        name="Lat-Lon Map Projection",
    )
    save_world(name=name, parameters=world_params, mesh=pc_mesh)

    # HACK: End hackathon!

    # Save mesh and world data.

    if save:
        std_con.print("Saving world.\r\n")

        save_world(name=name, parameters=world_params, mesh=world_mesh)

        save_timer_end: float = time.perf_counter()
        save_timer: float = save_timer_end - gen_timer_end

        std_con.print(f"World saved in {save_timer:0.4f} seconds.\r\n")

    # Visualization.

    if visualize:
        std_con.print("Starting visualization.\r\n")
        std_con.print("Close visualization window to end program.\r\n")

        viz(
            mesh=world_mesh,
            name=name,
            scalars="Elevations",
            radius=radius,
            zscale=scale,
            zmin=zmin,
            zmax=zmax,
        )

    std_con.print("Done.\r\n")


if __name__ == "__main__":
    typer.run(function=main)
