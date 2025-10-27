# Retro Desktop Application

A cross-platform desktop GUI for the Retro Game Package Manager.

## 🚀 Quick Start

### Option 1: Run from Source (Requires Python)

```bash
# Install
pip install .

# Launch GUI
retro-gui

# Or use CLI
retro update
retro search mario
```

### Option 2: Standalone Executables (No Python Required)

Download pre-built executables:
- **Windows**: `Retro.exe`
- **Linux**: `Retro` (AppImage or binary)
- **macOS**: `Retro.app`

Or build yourself: See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## ✨ Features

### 🎮 Search & Install
- Real-time search across 49+ game systems
- Advanced filtering (system, keywords, exclusions)
- Batch installation with progress tracking
- Shows installation status

### 📚 Library Management  
- View all installed games by system
- Quick size calculations and stats
- Batch removal with confirmation
- Automatic directory organization

### 🛠️ Utilities
- **CHD Compression**: Reduce disc images by 50-70%
- **Duplicate Removal**: Keep best versions based on region priority
- **Console Output**: Real-time operation feedback

## 📋 System Requirements

| Platform | Requirements |
|----------|-------------|
| **Windows** | Windows 7+ (64-bit) |
| **Linux** | Any modern distro with glibc 2.17+ |
| **macOS** | macOS 10.12+ (Sierra or later) |
| **RAM** | 2GB minimum, 4GB recommended |
| **Storage** | 100MB app + game storage (varies) |
| **Internet** | Required for downloading games |

## 🎯 Usage Examples

### Search Syntax

```
mario              → All Mario games
mario nes          → Mario games for NES only  
all snes           → All SNES games
sonic -demo -beta  → Sonic games without demos/betas
zelda gba -japan   → Zelda GBA games excluding Japanese versions
```

### Region Priority

When cleaning duplicates, the tool prefers:
1. **W** (World) - International releases
2. **E** (Europe) - PAL region
3. **U** (USA) - NTSC region  
4. **J** (Japan) - Japanese releases

## 🏗️ Building Executables

### Windows
```batch
build_windows.bat
```
Output: `dist/Retro.exe`

### Linux
```bash
./build_linux.sh
```
Output: `dist/Retro`

### macOS
```bash
./build_macos.sh
```
Output: `dist/Retro.app`

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for details.

## ⚙️ Configuration

Settings are stored in:
- **Windows**: `%USERPROFILE%\.config\retro\`
- **Linux/macOS**: `~/.config/retro/`

### Files
- `settings.json` - User preferences
- `systems.json` - Game systems and sources
- `packages.json` - Cached game database

### Default Settings
```json
{
  "roms_dir": "~/roms",
  "fetch_workers": 10,
  "install_workers": 20,
  "convert_workers": 4,
  "compress_workers": 4
}
```

## 🐛 Troubleshooting

### GUI Won't Start

**Python version issue:**
```bash
python --version  # Must be 3.7+
```

**tkinter not installed (Linux):**
```bash
sudo apt install python3-tk     # Ubuntu/Debian
sudo dnf install python3-tkinter # Fedora
sudo pacman -S tk                # Arch
```

**macOS with pyenv:**
```bash
env PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I/usr/local/opt/tcl-tk/include' --with-tcltk-libs='-L/usr/local/opt/tcl-tk/lib -ltcl8.6 -ltk8.6'" pyenv install 3.11.0
```

### "Could not load systems.json"

1. Click **"Update Database"** button
2. Check internet connection
3. Verify file permissions for config directory

### Installation Fails

- Check disk space: ROMs can be large (PSX games are 500MB+ each)
- Verify write permissions to ROMs directory
- Some repositories may be slow - be patient
- Check firewall/antivirus isn't blocking downloads

### Slow Performance

**Slow search:**
- Database needs updating: click "Update Database"
- Large collection: this is normal with 10,000+ games

**Slow downloads:**
- Adjust workers in Settings (try 10-30)
- Check internet speed
- Repository server may be slow

## 📚 Supported Systems

The tool supports 49+ systems including:

**Nintendo**: GB, GBC, GBA, NES, SNES, N64, DS, 3DS, GC, Wii, Wii U  
**Sony**: PSX, PS2, PS3, PSP, PS Vita  
**Sega**: Genesis, Saturn, Dreamcast, Game Gear  
**Microsoft**: Xbox, Xbox 360  
**Other**: Atari, Commodore, Neo Geo, Arcade, and more

See `systems.json` for complete list and sources.

## 🔧 Advanced Usage

### Adding Custom Systems

Edit `~/.config/retro/systems.json`:

```json
{
  "custom": {
    "name": "Custom System",
    "format": ["rom", "bin"],
    "url": [
      "https://example.com/roms/"
    ]
  }
}
```

### Portable Installation

For USB drive usage, modify `retro/main.py`:

```python
# Change this:
config_dir = os.path.expanduser("~/.config/retro")

# To this:
config_dir = os.path.join(os.path.dirname(__file__), "config")
```

### Automation via CLI

The CLI version (`retro`) can be used for scripts:

```bash
# Update database
retro update

# Install specific games
retro install "sonic genesis"

# Bulk operations
retro install all gba
retro remove all psx

# Compression pipeline
retro compress
retro autoremove
```

## 🤝 Contributing

Want to add features or fix bugs?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on your platform
5. Submit a pull request

## ⚖️ Legal Notice

**IMPORTANT**: This tool is for managing legally owned games only.

- Only download games you own physically
- Respect copyright laws in your country
- Some games are in public domain or freeware
- Developers are not responsible for misuse

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Credits

Built with:
- **Python** - Core language
- **tkinter** - GUI framework
- **PyInstaller** - Executable builder
- **requests** - HTTP downloads
- **BeautifulSoup** - HTML parsing
- **py7zr/rarfile** - Archive extraction

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See README.md and wiki
- **Community**: Join discussions on GitHub

---

**Made with ❤️ for retro gaming enthusiasts**

