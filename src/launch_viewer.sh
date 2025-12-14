#!/bin/bash
# Launcher for Lathe Desktop Viewer
# Fixes Qt/Wayland compatibility issues

export QT_QPA_PLATFORM=xcb
python -m lathe.viz.desktop "$@"
