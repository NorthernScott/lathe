import pyvista as pv

def viz(mesh: type[pv.PolyData], radius: int, zscale: int, zmin: int, zmax: int, scalars: type[pv.PolyData.point_data], name: str) -> None:
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
