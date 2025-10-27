# Retro GUI - Desktop Application

Desktop GUI version of the Retro Game Package Manager.

## Running the GUI

### From Python

After installing the package:

```bash
pip install .
retro-gui
```

Or run directly:

```bash
python -m retro.gui
```

### Standalone Executable

Build platform-specific executables using the build scripts (see `BUILD_INSTRUCTIONS.md`).

## Features

### Search & Install Tab
- **Search Games**: Search for games across all systems
- **Filter by System**: Include system name in search (e.g., "mario nes")
- **Exclude Terms**: Use minus prefix (e.g., "sonic -demo -beta")
- **Batch Installation**: Select multiple games and install at once
- **Installation Status**: See which games are already installed

### Installed Games Tab
- **View Collection**: Browse all installed games by system
- **Size Information**: See file sizes for each game
- **Batch Removal**: Select and remove multiple games
- **Quick Stats**: View total games and storage used

### Utilities Tab
- **CHD Compression**: Convert ISO/CUE/GDI files to compressed CHD format
- **Duplicate Removal**: Automatically remove duplicate ROMs based on region priority
- **Console Output**: View progress and results of operations

## Interface Guide

### Search Examples

| Search Query | Result |
|-------------|--------|
| `mario` | All games with "mario" in the name |
| `mario nes` | Mario games for NES only |
| `all snes` | All SNES games |
| `sonic -demo` | Sonic games excluding demos |
| `zelda -beta -prototype` | Zelda games excluding betas and prototypes |

### Keyboard Shortcuts

- **Enter** in search box: Perform search
- **Click on game**: Toggle selection checkbox

### Settings

Access via **File → Settings**:
- **ROMs Directory**: Where games are stored (default: `~/roms`)
- **Fetch Workers**: Number of concurrent threads for fetching (default: 10)
- **Install Workers**: Number of concurrent downloads (default: 20)

## System Requirements

- **Operating System**: Windows 7+, macOS 10.12+, or Linux (any modern distro)
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: Varies by collection size (ROMs can be 100GB+)
- **Internet**: Required for downloading games

## Screenshots

### Search & Install
Browse and install games with real-time search filtering.

### Installed Games
Manage your collection with easy selection and removal.

### Utilities
Compress ROMs and clean duplicates to save space.

## Tips

1. **First Run**: Click "Update Database" to fetch game listings
2. **Storage Management**: Use CHD compression to reduce disc-based game sizes by 50-70%
3. **Duplicate Cleanup**: Run "Clean Duplicates" to keep only the best version of each game
4. **Region Priority**: W (World) > E (Europe) > U (USA) > J (Japan)
5. **Batch Operations**: Select multiple games for faster processing

## Troubleshooting

### GUI doesn't start
- Check Python version: `python --version` (need 3.7+)
- Verify tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt install python3-tk`

### "Could not load systems.json"
- Click "Update Database" to download system definitions
- Check internet connection

### Installation fails
- Verify write permissions to ROMs directory
- Check available disk space
- Review console output in Utilities tab

### Slow downloads
- Adjust "Install Workers" in Settings
- Check internet connection speed
- Some servers may have rate limits

## Advanced Usage

### Custom Systems
Edit `~/.config/retro/systems.json` to add custom game sources:

```json
{
  "custom_system": {
    "name": "Custom System",
    "format": ["rom", "bin"],
    "url": ["https://example.com/games/"]
  }
}
```

### Portable Mode
To run from USB drive, edit `retro/main.py` and change:
```python
config_dir = os.path.expanduser("~/.config/retro")
```
to:
```python
config_dir = os.path.join(os.path.dirname(__file__), "config")
```

## Legal Notice

This tool is for managing legally owned games only. Always respect copyright laws and intellectual property rights. The developers are not responsible for any misuse of this software.

