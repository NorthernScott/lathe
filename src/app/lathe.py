# -*- coding: utf-8 -*-


# import core modules
import json
import logging
import random
import time
from io import TextIOWrapper
from typing import Generator

import numpy as np
import typer
from rich.logging import RichHandler
from rich.table import Table
from typing_extensions import Annotated

from mylogger import log, std_con
from terrain import arr_sample_noise, sample_octaves
from util import Mesh, MeshArray, create_mesh, now, rescale, save_world
from viz import viz

# Define globals.

RADIUS: int = 6378100  # Radius of the world in meters. The approximate radius of Earth is 6378100 m.
FEATURE_SIZE: np.float64 = (
    RADIUS * 0.5
)  # Determines the "coherence" of the random noise; affects the size of discrete landmasses. A good size for Earth-like continents is 0.5× the radius.
ZMIN: int = round(
    number=-(RADIUS * 0.0015)
)  # The lowest elevation in the world, in meters. The deepest oceanic trench on Earth is approximately -10,300 m.
ZMAX: int = round(
    number=RADIUS * 0.0015
)  # The highest elevation in the world, in meters. The highest peak on Earth is approximately 8700 m.
ZRANGE: float = ZMAX - ZMIN
ZTILT: float = 23.4  # Used in mapping spherical coordinates to lat-lon coordinates in a Coordinate Reference System (CRS). The present z-axis tilt of the Earth is approximately 23.4 degrees.
ZSCALE: int = 1  # A scaling factor for elevations to make them visible in the plot.
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
    f: TextIOWrapper = open(file="planetnames.json", mode="rt")
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
        typer.Option(help="Sets whether the world data is saved to an output file."),
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
    feature_size: Annotated[
        float,
        typer.Option(
            help="Determines the coherence of noise; affects the size of discrete landmasses. A good size for Earth-like continents is approximately 50% of the radius."
        ),
    ] = FEATURE_SIZE,
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
            help="Sets the global sea level by defining a relative percent of the range from min to max altitude."
        ),
    ] = OCEAN_PERCENT,
    zscale: Annotated[
        int,
        typer.Option(
            help="Sets a scaling factor for elevations to make them visible in the plot. Does not change the actual elevation values."
        ),
    ] = ZSCALE,
    octaves: Annotated[
        int,
        typer.Option(help="Sets the number of octaves to use for noise sampling."),
    ] = OCTAVES,
    loglevel: Annotated[
        str, typer.Option(help="Sets the verbosity of the logger.")
    ] = LOGLEVEL,
    platesnum: Annotated[
        int, typer.Option(help="Sets the number of tectonic plates to create.")
    ] = PLATESNUM,
) -> None:
    """A program to procedurally generate worlds.

    Returns:

        A 3D icosphere mesh with elevation data provided in cartesian coordinates.
    """

    # Setup logger.

    logging.basicConfig(
        level=loglevel,
        format=LOGFORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )

    log.debug(msg="Initialize logger.")

    log.debug(msg="Initialize timer.")
    timer_start: float = time.perf_counter()

    # Begin generation.

    std_con.print("Beginning terrain noise generation.\r\n")

    # Set world seed and parameters.

    std_con.print("Setting world seed and parameters.\r\n")

    if seed == 0:
        seed_rng: Generator = np.random.default_rng()
        world_seed: int = seed_rng.integers(low=0, high=999999)
    else:
        world_seed: int = seed

    zrange: float = zmax - zmin

    ocean_point: float = ocean_percent * zrange

    # Create world_params dictionary.

    world_params = {
        "name": name,
        "timestamp": now(),
        "seed": world_seed,
        "radius": radius,
        "feature size": feature_size,
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
    params_table.add_row("World Seed", str(object=world_seed))
    params_table.add_row("Radius", str(object=radius))
    params_table.add_row("Feature Size", str(object=feature_size))
    params_table.add_row("Recursion Factor", str(object=recursion))
    params_table.add_row("Octaves (#)", str(object=octaves))
    params_table.add_row("Axial Tilt", str(object=ztilt))
    params_table.add_row("Lowest Elevation", str(object=zmin))
    params_table.add_row("Highest Elevation", str(object=zmax))
    params_table.add_row("Elevation Range", str(object=zrange))
    params_table.add_row("Ocean Percent", str(object=ocean_percent))
    params_table.add_row("Sea Level", str(object=ocean_point))
    params_table.add_row("Log Display", str(object=loglevel))

    std_con.print(params_table)

    # TODO: Determine how ocean_percent impacts surface area water cover.
    # NOTE: Ocean_percent essentially sets a surface water level for the display mask. I'm not sure it's actually necessary to set a water mask, since we assume that sea level = 0 m. Our rescale function handles this, and we should be able to change the map display accordingly. That said, a value to set the water level or % of surface covered by ocean would be helpful. I need to understand how this value relates to that. For reference, the percentage of the Earth's surface covered by water is approximately 71%.

    # Create world mesh, points arrays, and faces arrays.

    std_con.print("Creating world mesh.\r\n")

    world_mesh: Mesh = create_mesh(radius=radius, recursion=recursion, ztilt=ztilt)

    std_con.print(world_mesh, "\r\n")

    log.debug(msg="Points Array:")
    log.debug(msg=world_mesh.points)
    log.debug(msg="")

    log.debug(msg="Faces Array:")
    log.debug(msg=world_mesh.faces)
    log.debug(msg="")

    # Generate elevations.

    std_con.print("Generating elevations.\r\n")

    raw_elevations: MeshArray = arr_sample_noise(
        world_mesh=world_mesh,
        roughness=INIT_ROUGHNESS,
        strength=INIT_STRENGTH,
        feature_size=feature_size,
        radius=radius,
        world_seed=world_seed,
    )

    # raw_elevations: MeshArray = sample_octaves(
    #     points=world_mesh.points,
    #     octaves=octaves,
    #     init_roughness=INIT_ROUGHNESS,
    #     init_strength=INIT_STRENGTH,
    #     roughness=ROUGHNESS,
    #     persistence=PERSISTENCE,
    #     feature_size=feature_size,
    #     radius=radius,
    # )

    log.debug(msg="Raw elevations:")
    log.debug(msg=raw_elevations)
    log.debug(msg="")

    # Rescale elevations.

    std_con.print("Rescaling elevations.\r\n")

    rescaled_elevations: np.NDArray = rescale(
        elevations=raw_elevations, zmin=zmin, zmax=zmax
    )

    log.debug(msg="Rescaled Elevations:")
    log.debug(msg=rescaled_elevations)
    log.debug(msg="")

    # Create elevation scalars including a z_scale factor to make elevations visible.

    std_con.print("Applying elevations to mesh.\r\n")

    log.debug(msg="Generating elevation scalars.")
    elevation_scalars: np.NDArray = ((rescaled_elevations * zscale) + radius) / radius
    log.debug(msg="")

    log.debug(msg="Elevation Scalars:")
    log.debug(msg=elevation_scalars)
    log.debug(msg="")

    # Apply elevation scalars to mesh.

    log.debug(msg="Applying elevations.")
    # world_mesh.points[:, 0] *= elevation_scalars
    # world_mesh.points[:, 1] *= elevation_scalars
    world_mesh.points[:, 2] *= elevation_scalars
    log.debug(msg=world_mesh.points)
    log.debug(msg="")

    # Add rescaled elevations (without z_scale factor) to mesh points data.

    log.debug(msg="Adding elevations to mesh dataset.")
    world_mesh.point_data["Elevation"] = rescaled_elevations
    log.debug(msg="")

    log.debug(msg="Mesh Point Data:")
    log.debug(msg=world_mesh.point_data)
    log.debug(msg="")

    timer_end: float = time.perf_counter()
    timer: float = timer_end - timer_start

    std_con.print(f"Terrain generated in {timer:0.4f} seconds.\r\n")

    # Save routine. Checks if 'outputs' dir exists and creates if not.

    if save:
        std_con.print("Saving world config.\r\n")
        save_world(name=name, parameters=world_params, mesh=world_mesh)

    # Visualization.

    log.info(msg="Starting vizualization.")
    viz(
        world_mesh=world_mesh,
        scalars="Elevations",
        radius=radius,
        zscale=ZSCALE,
        zmin=zmin,
        zmax=zmax,
    )

    log.debug(msg="Done main thread.")

    return None


if __name__ == "__main__":
    typer.run(function=main)
