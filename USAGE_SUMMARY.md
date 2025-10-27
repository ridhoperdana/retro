# Retro - Quick Reference

## Installation

```bash
pip install .
```

## Usage

### Command Line (CLI)

```bash
# Update game database
retro update

# Search games
retro search mario
retro search "sonic" genesis
retro search zelda -demo -beta

# Install games
retro install mario nes
retro install all gba

# List installed games
retro list

# Remove games
retro remove sonic
retro remove all psx

# Utilities
retro compress      # Convert to CHD
retro autoremove    # Remove duplicates
```

### Desktop GUI

```bash
retro-gui
```

**Features:**
- Search & Install games with visual interface
- Manage installed games
- CHD compression & duplicate removal
- Real-time progress tracking

## Building Standalone Executables

```bash
# Windows
build_windows.bat

# Linux
./build_linux.sh

# macOS
./build_macos.sh
```

Output in `dist/` folder - no Python required!

## Configuration

Location: `~/.config/retro/`

**settings.json:**
```json
{
  "roms_dir": "~/roms",
  "fetch_workers": 10,
  "install_workers": 20
}
```

**systems.json** - Add custom systems:
```json
{
  "custom_system": {
    "name": "My System",
    "format": ["rom"],
    "url": ["https://example.com/roms/"]
  }
}
```

## Search Patterns

| Pattern | Result |
|---------|--------|
| `mario` | All Mario games |
| `mario nes` | Mario on NES only |
| `all snes` | Every SNES game |
| `sonic -demo` | Sonic, no demos |
| `zelda gba -japan` | Zelda GBA, no Japan |

## Tips

1. **First time**: Run `retro update` or click "Update Database" in GUI
2. **Save space**: Use `retro compress` (CHD format saves 50-70%)
3. **Remove duplicates**: Use `retro autoremove` (keeps best version)
4. **Portable**: Edit config_dir in main.py for USB drive usage
5. **Multiple systems**: Search with system name for faster results

## Troubleshooting

**"Could not load systems.json"**
→ Run `retro update` first

**tkinter not found (GUI)**
→ `sudo apt install python3-tk` (Linux)
→ Build standalone executable instead

**Slow downloads**
→ Increase install_workers in settings.json

**Installation fails**
→ Check disk space and permissions

## Documentation

- **README.md** - Complete documentation
- **DESKTOP_APP.md** - Desktop app guide
- **BUILD_INSTRUCTIONS.md** - Building executables
- **README_GUI.md** - GUI features

## Legal

Only download games you legally own. Respect copyright laws.

## Support

Report issues: GitHub Issues
Documentation: Project wiki

