from engine.world import World
from engine.viz import Visualizer

test = World()
test.generate_elevations()
test.create_tectonic_plates(12)
print(test.mesh)

v = Visualizer(test, name=test.name, radius=test.radius, zscale=test.zscale)
v.viz()
