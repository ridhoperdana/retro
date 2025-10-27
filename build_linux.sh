#!/bin/bash
echo "Building Retro for Linux..."
pip install pyinstaller
pyinstaller retro.spec --clean
echo ""
echo "Build complete! Executable is in the dist/ folder"

