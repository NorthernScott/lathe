# -*- coding: utf-8 -*-

# import core libraries.
import json
import logging
import os
import random
import time
from io import TextIOWrapper

# import third-party modules
import numpy as np
import typer
from typing_extensions import Annotated
from numpy.typing import NDArray
from rich.logging import RichHandler
from rich.table import Table

# import internal modules
from mylogger import err_con, std_con
from terrain import sample_octaves
from util import Mesh, MeshArray, create_mesh, now, rescale, save_world, xyz2latlon
from viz import viz

# Define global defaults.
RADIUS: int = 6378100  # Radius of the world in meters. The approximate radius of Earth is 6378100 m.
ZMIN: int = round(
    number=-(RADIUS * 0.0015)
)  # The lowest elevation in the world, in meters. The deepest oceanic trench on Earth is approximately -10,300 m.
ZMAX: int = round(
    number=RADIUS * 0.0015
)  # The highest elevation in the world, in meters. The highest peak on Earth is approximately 8700 m.
ZRANGE: float = ZMAX - ZMIN
ZTILT: float = 23.4  # Used in mapping spherical coordinates to lat-lon coordinates in a Coordinate Reference System (CRS). The present z-axis tilt of the Earth is approximately 23.4 degrees.
ZSCALE: int = 20  # A scaling factor for elevations to make them visible in the plot.
OCEAN_PERCENT: float = 0.55  # Sets the point of elevation 0 as a relative percent of the range from zmin to zmax during rescaling.
OCEAN_POINT: float = OCEAN_PERCENT * ZRANGE
RECURSION: int = 9  # The number of recursions used in creating the icosphere mesh. 9 yields 2,621,442 points and 5,242,880 cells. Surface area of the Earth is approximately 514 million km2.
OCTAVES: int = 8  # Sets the number of iterations to use for noise sampling, resulting in a more complex output.
LOGLEVEL: str = "WARNING"
LOGFORMAT: str = "\r\n%(message)s"
INIT_ROUGHNESS: float = (
    1.5  # Sets the initial roughness (frequency) of the first octave of noise.
)
INIT_STRENGTH: float = (
    0.4  # Sets the initial strength (amplitude) of the first octave of noise.
)
ROUGHNESS: float = 2.5  # Multiply roughness by this much per octave.
PERSISTENCE: float = 0.5  # Multiply strength by this much per octave.
PLATESNUM: int = round(
    number=RADIUS / 500_000
)  # The number of tectonic plates to generate. The Earth has approximately 12 major plates.


# Setup functions.


def getPlanetName() -> str:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "planetnames.json")
    f: TextIOWrapper = open(file=file_path, mode="rt")
    data = json.load(fp=f)
    names = data["planetNames"]

    return random.choice(seq=names)


# Main thread.


def main(
    name: Annotated[
        str,
        typer.Argument(
            default_factory=getPlanetName,
            help="A name for the world. If one is not provided, a random name will be set.",
        ),
    ],
    save: Annotated[
        bool,
        typer.Option(
            help="Sets whether the mesh and world data are saved to output files."
        ),
    ] = False,
    seed: Annotated[
        int,
        typer.Option(help="The world seed to be used. Defaults to a random integer."),
    ] = 0,
    radius: Annotated[
        int,
        typer.Option(
            help="The radius of the world in meters. (Earth radius is approximately 6378100 m.)"
        ),
    ] = RADIUS,
    recursion: Annotated[
        int,
        typer.Option(
            help="The number of recursions used in creating the icosphere mesh. 9 yields 2,621,442 points and 5,242,880 cells. The surface area of the Earth is approximately 514 million km2"
        ),
    ] = RECURSION,
    ztilt: Annotated[
        float,
        typer.Option(
            help="Controls the z-axis tilt of the planet. The Earth's axial tilt is (currently) approximately 23.4 degrees."
        ),
    ] = ZTILT,
    zmin: Annotated[
        int,
        typer.Option(
            help="The lowest elevation value on the planet. The deepest oceanic trench on Earth is approximately -10300 m"
        ),
    ] = ZMIN,
    zmax: Annotated[
        int,
        typer.Option(
            help="The highest elevation value on the planet. The highest peak on Earth is approximately 8700 m."
        ),
    ] = ZMAX,
    ocean_percent: Annotated[
        float,
        typer.Option(
            help="Sets the global sea level by defining a relative percent of the range from min to max elevation."
        ),
    ] = OCEAN_PERCENT,
    scale: Annotated[
        int,
        typer.Option(
            help="Sets a scaling factor for elevations to make them visible in the plot. Does not change the actual elevation values."
        ),
    ] = ZSCALE,
    octaves: Annotated[
        int,
        typer.Option(
            help='Sets the number of octaves to use for noise sampling. More octaves create more "complexity."'
        ),
    ] = OCTAVES,
    loglevel: Annotated[
        str, typer.Option(help="Sets the verbosity of the logger.")
    ] = LOGLEVEL,
    platesnum: Annotated[
        int,
        typer.Option(
            help="Sets the number of tectonic plates to create. --Not currently in use.--"
        ),
    ] = PLATESNUM,
) -> None:
    """
    Main function for the Lathe program. Generates a 3D mesh of a planet, applies elevations, and visualizes the result.

    Args:
        name (Annotated[ str, typer.Argument, optional): A name for the world. If one is not provided, a random name will be set. Defaults to a random value provided by the getPlanetName() function.
        save (Annotated[ bool, typer.Option, optional): Sets whether the mesh and world data are saved to output files. Defaults to False.
        seed (Annotated[ int, typer.Option, optional): The world seed to be used. Defaults to 0, which triggers selection of a random integer.
        radius (Annotated[ int, typer.Option, optional): The radius of the world in meters. (Earth radius is approximately 6378100 m.) Defaults to the value of RADIUS.
        recursion (Annotated[ int, typer.Option, optional): The number of recursions used in creating the icosphere mesh. '9' yields 2,621,442 points and 5,242,880 cells. The surface area of the Earth is approximately 514 million km2. Defaults to the value of RECURSION.
        ztilt (Annotated[ float, typer.Option, optional): Controls the z-axis tilt of the planet. The Earth's axial tilt is (currently) approximately 23.4 degrees. Defaults to ZTILT.
        zmin (Annotated[ int, typer.Option, optional): The lowest elevation value on the planet. The deepest oceanic trench on Earth is approximately -10300 m. Defaults to ZMIN.
        zmax (Annotated[ int, typer.Option, optional): The highest elevation value on the planet. The highest peak on Earth is approximately 8700 m. Defaults to ZMAX.
        ocean_percent (Annotated[ float, typer.Option, optional): Sets the global sea level by defining a relative percent of the range from min to max elevation. Defaults to OCEAN_PERCENT.
        scale (Annotated[ int, typer.Option, optional): Sets a scaling factor for elevations to make them visible in the plot. Does not change the actual elevation values. Defaults to ZSCALE.
        octaves (Annotated[ int, typer.Option, optional): Sets the number of octaves to use for noise sampling. More octaves create more "complexity." Defaults to OCTAVES.
        loglevel (Annotated[ str, typer.Option, optional): Sets the verbosity of the logger. Defaults to LOGLEVEL.
        platesnum (Annotated[ int, typer.Option, optional): Sets the number of tectonic plates to create. --Not currently in use.-- Defaults to PLATESNUM.

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
        if seed == 0:
            world_seed = 0
        elif seed < 1:
            world_seed = 0
            err_con.print(
                "Seed must be an integer between 1 and 255. Setting to random seed.\r\n"
            )
        elif seed > 255:
            world_seed = 0
            err_con.print(
                "Seed must be an integer between 1 and 255. Setting to random seed.\r\n"
            )
        else:
            world_seed = seed
    except ValueError as e:
        err_con.print(f"Seed {e} is not an integer between 1 and 256.\r\n")
    finally:
        if world_seed == 0:
            world_seed_string = str("Random")
        else:
            world_seed_string = str(world_seed)

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

    # TODO: Determine how ocean_percent impacts surface area water cover.
    # NOTE: Ocean_percent essentially sets a surface water level for the display mask. I'm not sure it's actually necessary to set a water mask, since we assume that sea level = 0 m. Our rescale function handles this, and we should be able to change the map display accordingly. That said, a value to set the water level or % of surface covered by ocean would be helpful. I need to understand how this value relates to that. For reference, the percentage of the Earth's surface covered by water is approximately 71%.

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

    rescaled_elevations: NDArray[np.float64] = rescale(
        elevations=raw_elevations, zmin=zmin, zmax=zmax
    )

    std_con.print(f"Sample of Rescaled Elevations:\r\n {rescaled_elevations} \r\n")

    # Add rescaleq elevations to mesh as scalar dataset.

    std_con.print("Adding rescaled elevations to mesh as scalar dataset.\r\n")

    world_mesh.point_data["Elevations"] = rescaled_elevations

    std_con.print(
        f"Sample of Elevations Dataset:\r\n {world_mesh.point_data['Elevations']} \r\n"
    )

    # Display world generation time.

    gen_timer_end: float = time.perf_counter()
    gen_timer: float = gen_timer_end - timer_start

    std_con.print(f"Terrain generated in {gen_timer:0.4f} seconds.\r\n")

    # XYZ to Lat-Lon conversion.

    std_con.print("Converting XYZ to Lat-Lon coordinates.\r\n")

    coords = xyz2latlon(mesh=world_mesh)

    std_con.print("Adding lat-lon coordinates to mesh as dataset.\r\n")

    world_mesh.point_data["LatLon"] = coords

    std_con.print(
        f"Sample of LatLon Dataset:\r\n {world_mesh.point_data['LatLon']} \r\n"
    )

    latlon_timer_end: float = time.perf_counter()
    latlon_timer: float = latlon_timer_end - gen_timer_end

    std_con.print(f"Lat-Lon coordinates generated in {latlon_timer:0.4f} seconds.\r\n")

    # Save mesh and world data.

    if save:
        std_con.print("Saving world.\r\n")

        save_world(name=name, parameters=world_params, mesh=world_mesh)

        save_timer_end: float = time.perf_counter()
        save_timer: float = save_timer_end - gen_timer_end

        std_con.print(f"World saved in {save_timer:0.4f} seconds.\r\n")

    # Visualization.

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

    return None


if __name__ == "__main__":
    typer.run(function=main)