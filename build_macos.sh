#!/bin/bash
echo "Building Retro for macOS..."
pip install pyinstaller
pyinstaller retro.spec --clean
echo ""
echo "Build complete! Application is in the dist/ folder"
echo "To create a DMG: hdiutil create -volname Retro -srcfolder dist/Retro.app -ov -format UDZO dist/Retro.dmg"

