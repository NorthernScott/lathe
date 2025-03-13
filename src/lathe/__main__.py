import os
import sys
from pathlib import Path

from lathe.engine.viz import Visualizer
from lathe.engine.world import World

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package
    package_source_path: Path = Path(__file__).parent
    sys.path.insert(0, str(object=package_source_path))

if __name__ == "__main__":
    test = World(recursion=5)
    test.generate_elevations()
    test.create_tectonic_plates(num_plates=12)
    print(test.mesh)

    Visualizer(world=test)
