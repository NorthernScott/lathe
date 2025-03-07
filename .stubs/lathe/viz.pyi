from _typeshed import Incomplete
from lathe.world import World as World

class Visualizer:
    world_name: Incomplete
    world_radius: Incomplete
    world_zscale: Incomplete
    scalar_datasets: Incomplete
    def __init__(self, world: World, name: str, radius: int, zscale: int) -> None: ...
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
