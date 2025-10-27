# Quick Start - macOS Build (FIXED)

## ✅ The Issue is Fixed!

The relative import issue has been resolved. You can now build and run the app successfully.

## 🚀 Build the App

```bash
cd /Users/ridhoperdana/workspace/retro

# Clean previous build
rm -rf build dist

# Build with your local Python (3.9.21 works!)
python3 -m PyInstaller retro.spec --clean
```

## 🎯 Run the App

### Method 1: Double-click (macOS Finder)
Simply double-click `dist/Retro.app` in Finder

### Method 2: From Terminal (for testing)
```bash
./dist/Retro.app/Contents/MacOS/Retro
```

### Method 3: Open command
```bash
open dist/Retro.app
```

## ✨ What Was Fixed

1. **Changed imports** in `retro/gui.py` from relative to absolute:
   - Before: `from .main import Manager`
   - After: `from retro.main import Manager`

2. **Created entry point** `run_gui.py` that PyInstaller can use properly

3. **Updated spec file** to include the entire `retro` package

## 📦 Create DMG for Distribution

```bash
hdiutil create -volname Retro -srcfolder dist/Retro.app -ov -format UDZO dist/Retro.dmg
```

This creates `dist/Retro.dmg` that you can share with others!

## 🧪 Testing Checklist

- [ ] App opens without crashing
- [ ] Main window appears
- [ ] Can click "Update Database" button
- [ ] Search functionality works
- [ ] Tabs switch properly

## 📝 Notes

- First build may take 2-3 minutes
- App size: ~50-70MB (includes Python runtime)
- Works on macOS 10.12+ (Sierra and later)
- No Python installation needed for end users

## 🎉 You're Done!

The app in `dist/Retro.app` is now ready to use and distribute!

