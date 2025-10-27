# macOS Build Troubleshooting

## Issue: App closes immediately when double-clicked

This happens when tkinter is not available in your Python installation.

### Quick Fix - Use the updated build script:

```bash
./build_macos_fix.sh
```

This script will automatically detect and fix tkinter issues.

---

## Manual Solutions

### Solution 1: Use System Python (Easiest)

macOS comes with Python that has tkinter built-in:

```bash
# Check if system Python has tkinter
/usr/bin/python3 -c "import tkinter"
# Should print nothing = success

# Install PyInstaller
/usr/bin/python3 -m pip install --user pyinstaller

# Build
/usr/bin/python3 -m PyInstaller retro.spec --clean
```

### Solution 2: Install Python with Homebrew

```bash
# Install Python with tkinter
brew install python-tk@3.11

# Install dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build
pyinstaller retro.spec --clean
```

### Solution 3: Rebuild pyenv Python with tkinter

If you're using pyenv:

```bash
# Install tcl-tk
brew install tcl-tk

# Get brew prefix (for Intel vs Apple Silicon)
TCL_PREFIX=$(brew --prefix tcl-tk)

# Reinstall Python with tkinter support
env PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I${TCL_PREFIX}/include' --with-tcltk-libs='-L${TCL_PREFIX}/lib -ltcl8.6 -ltk8.6'" pyenv install 3.11.11

# Set as global/local
pyenv global 3.11.11  # or: pyenv local 3.11.11

# Verify
python -c "import tkinter; print('✓ tkinter works!')"

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build
pyinstaller retro.spec --clean
```

---

## Verify Your Build

After building, test from terminal:

```bash
# Test the executable directly
./dist/Retro.app/Contents/MacOS/Retro
```

If it runs without errors, the app works!

---

## Common Errors

### "No module named '_tkinter'"

**Cause**: Python was built without tkinter  
**Solution**: Use one of the solutions above

### "console=False" causes crash

**Cause**: GUI apps on macOS need proper entitlements  
**Solution**: Already handled in retro.spec

### "dyld: Library not loaded"

**Cause**: Missing dynamic libraries  
**Solution**: PyInstaller should bundle these automatically. Try:

```bash
# Check what's missing
otool -L dist/Retro.app/Contents/MacOS/Retro
```

---

## Testing Your Python

Check if your Python has tkinter:

```bash
python -c "import tkinter; tkinter._test()"
```

This should open a small test window. If it does, your Python is fine!

---

## Alternative: Run from Python (No Build)

If building continues to fail, just run directly:

```bash
# Install
pip install .

# Run GUI
retro-gui
```

This requires Python but doesn't need PyInstaller.

---

## Still Having Issues?

1. **Check Python version**:
   ```bash
   python --version  # Need 3.7+
   ```

2. **Check tkinter**:
   ```bash
   python -c "import tkinter"
   ```

3. **Clean build**:
   ```bash
   rm -rf build dist *.spec
   pyinstaller retro.spec --clean
   ```

4. **Use verbose mode**:
   ```bash
   pyinstaller retro.spec --clean --log-level DEBUG
   ```

5. **Check Console.app** for crash logs:
   - Open Console.app
   - Search for "Retro"
   - Look for crash reports

---

## Working? Create DMG for Distribution

```bash
hdiutil create -volname Retro -srcfolder dist/Retro.app -ov -format UDZO dist/Retro.dmg
```

This creates a distributable DMG file!

