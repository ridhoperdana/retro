# Retro - Usage Guide

## Installation

```bash
pip install .
```

## Two Ways to Use

### 1. Web GUI (Recommended)

Beautiful browser-based interface:

```bash
retro-gui
```

Features:
- Modern gradient design
- Search and install games visually
- View your collection
- Real-time progress updates

### 2. Command Line (CLI)

For scripts and power users:

```bash
# Update game database
retro update

# Search games
retro search mario
retro search sonic genesis
retro search all gba

# Install games  
retro install mario nes
retro install all gameboy

# List installed
retro list

# Remove games
retro remove sonic
retro remove all psx

# Utilities
retro compress      # Convert to CHD
retro autoremove    # Remove duplicates
```

## Search Syntax

| Pattern | Result |
|---------|--------|
| `mario` | All Mario games |
| `mario nes` | Mario on NES |
| `all snes` | All SNES games |
| `sonic -demo` | Sonic, no demos |
| `zelda -beta -japan` | Zelda, no betas/JP |

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

**systems.json:**
Add custom systems or modify existing ones.

## Tips

1. **First time**: Run `retro update` or click "Update Database" in GUI
2. **Save space**: Use `retro compress` for CHD format (50-70% smaller)
3. **Clean up**: Use `retro autoremove` to remove duplicate ROMs
4. **Bulk install**: Search with `all SYSTEM` to get everything for a system

## Examples

### GUI Workflow
1. Run `retro-gui`
2. Click "Update Database"
3. Search for "mario"
4. Click "Yes" to install
5. Click "List Installed" to verify

### CLI Workflow
```bash
# Update database
retro update

# Find and install Sonic games
retro search sonic genesis
retro install sonic genesis

# Check what's installed
retro list

# Clean up
retro compress
retro autoremove
```

## Troubleshooting

**"No systems loaded"**
→ Run `retro update` first

**Web GUI won't start**
→ Check if Flask is installed: `pip install flask`

**Port 5000 busy**
→ Edit `retro/web_gui.py` and change port number

**Slow downloads**
→ Increase `install_workers` in `settings.json`

## Support

- **Issues**: Report on GitHub
- **CLI Help**: `retro --help`
- **Documentation**: See README.md

---

For more details, see:
- `README.md` - Full documentation
- `README_GUI.md` - Web GUI guide
- `systems.json` - Supported systems

