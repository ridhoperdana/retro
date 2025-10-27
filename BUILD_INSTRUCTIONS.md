# Building Standalone Executables

This guide shows you how to build standalone executables for Windows, Linux, and macOS.

## Prerequisites

1. **Python 3.7+** installed
2. **Install dependencies**:
   ```bash
   pip install .
   ```

## Building

### Windows

1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Run:
   ```batch
   build_windows.bat
   ```
4. Find the executable in `dist/Retro.exe`

### Linux

1. Open Terminal
2. Navigate to the project directory
3. Run:
   ```bash
   ./build_linux.sh
   ```
4. Find the executable in `dist/Retro`

### macOS

1. Open Terminal
2. Navigate to the project directory
3. Run:
   ```bash
   ./build_macos.sh
   ```
4. Find the application in `dist/Retro.app`

## Distribution

### Windows
- Distribute `dist/Retro.exe` directly
- Or create an installer using tools like Inno Setup or NSIS

### Linux
- Distribute the `dist/Retro` executable
- Or create a `.deb` or `.rpm` package using FPM

### macOS
- Distribute `dist/Retro.app`
- Or create a DMG:
  ```bash
  hdiutil create -volname Retro -srcfolder dist/Retro.app -ov -format UDZO dist/Retro.dmg
  ```

## Notes

- The first build may take several minutes
- Executables are self-contained and include Python runtime
- File sizes will be ~50-100MB depending on platform
- Antivirus software may flag the executable (false positive - you can submit for whitelisting)

## Troubleshooting

**"Module not found" errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**"Hidden imports missing":**
- Edit `retro.spec` and add missing modules to `hiddenimports`

**macOS "damaged" warning:**
- Run: `xattr -cr dist/Retro.app`
- Or right-click → Open instead of double-clicking

**Linux missing libraries:**
- Install system dependencies: `sudo apt install python3-tk` (Ubuntu/Debian)

