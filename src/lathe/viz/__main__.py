"""Main entry point for visualization module."""

import os

# Fix Qt platform for Wayland/X11 compatibility
# PyVista/VTK works better with X11 (xcb) than native Wayland
if not os.environ.get('QT_QPA_PLATFORM'):
    os.environ['QT_QPA_PLATFORM'] = 'xcb'

from lathe.viz.desktop import main

if __name__ == "__main__":
    main()
