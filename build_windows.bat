@echo off
echo Building Retro for Windows...
python -m pip install pyinstaller
pyinstaller retro.spec --clean
echo.
echo Build complete! Executable is in the dist/ folder
pause

