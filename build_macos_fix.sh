#!/bin/bash

echo "Building Retro for macOS (with tkinter fix)..."
echo ""

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter is not available in your Python installation"
    echo ""
    echo "Solutions:"
    echo ""
    echo "1. Use system Python (recommended):"
    echo "   /usr/bin/python3 -m pip install --user pyinstaller"
    echo "   /usr/bin/python3 -m PyInstaller retro.spec --clean"
    echo ""
    echo "2. Install Python with tkinter via Homebrew:"
    echo "   brew install python-tk@3.11"
    echo "   brew link python-tk@3.11"
    echo ""
    echo "3. Rebuild pyenv Python with tkinter:"
    echo "   brew install tcl-tk"
    echo "   env PYTHON_CONFIGURE_OPTS=\"--with-tcltk-includes='-I/opt/homebrew/opt/tcl-tk/include' --with-tcltk-libs='-L/opt/homebrew/opt/tcl-tk/lib -ltcl8.6 -ltk8.6'\" pyenv install 3.11.11"
    echo ""
    echo "Attempting to use system Python..."
    echo ""
    
    # Try system Python
    /usr/bin/python3 -c "import tkinter" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✓ System Python has tkinter!"
        echo "Installing PyInstaller..."
        /usr/bin/python3 -m pip install --user pyinstaller
        echo ""
        echo "Building with system Python..."
        /usr/bin/python3 -m PyInstaller retro.spec --clean
    else
        echo "❌ System Python also doesn't have tkinter"
        exit 1
    fi
else
    echo "✓ tkinter is available"
    pip install pyinstaller
    pyinstaller retro.spec --clean
fi

echo ""
if [ -f "dist/Retro.app/Contents/MacOS/Retro" ]; then
    echo "✅ Build complete! Application is in dist/Retro.app"
    echo ""
    echo "To test: ./dist/Retro.app/Contents/MacOS/Retro"
    echo "To create DMG: hdiutil create -volname Retro -srcfolder dist/Retro.app -ov -format UDZO dist/Retro.dmg"
else
    echo "❌ Build failed"
    exit 1
fi

