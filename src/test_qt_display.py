"""Test Qt and PyVista display."""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from pyvistaqt import QtInteractor
import pyvista as pv

def test_simple_qt():
    """Test simple Qt window."""
    print("Testing simple Qt window...")
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Simple Qt Test")
    window.setGeometry(100, 100, 800, 600)

    central = QWidget()
    window.setCentralWidget(central)

    layout = QVBoxLayout(central)
    layout.addWidget(QLabel("If you see this, Qt is working!"))

    window.show()
    print("✓ Qt window created successfully")
    window.close()
    app.quit()

def test_pyvista_qt():
    """Test PyVista with Qt."""
    print("\nTesting PyVista + Qt integration...")

    # Ensure PyVista is not in off-screen mode
    pv.OFF_SCREEN = False

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("PyVista Qt Test")
    window.setGeometry(100, 100, 800, 600)

    central = QWidget()
    window.setCentralWidget(central)

    layout = QVBoxLayout(central)

    # Create QtInteractor
    plotter = QtInteractor(central)
    layout.addWidget(plotter)

    # Add a simple sphere
    sphere = pv.Sphere()
    plotter.add_mesh(sphere, color='red')
    plotter.set_background('white')

    window.show()
    print("✓ PyVista QtInteractor created successfully")

    # Don't exec - just test creation
    window.close()
    app.quit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", choices=["qt", "pyvista"], default="pyvista")
    args = parser.parse_args()

    try:
        if args.test == "qt":
            test_simple_qt()
        else:
            test_pyvista_qt()
        print("\n✓ Test passed!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
