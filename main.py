from engine.world import World
from engine.viz import Visualizer

test = World(recursion=5)
test.generate_elevations()
test.create_tectonic_plates(12)
print(test.mesh)

v = Visualizer(test)
v.viz()
