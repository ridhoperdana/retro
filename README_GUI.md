# Retro Web GUI

A beautiful web-based interface for the Retro Game Package Manager.

## 🚀 Quick Start

### Installation

```bash
pip install .
```

### Running the GUI

```bash
retro-gui
```

Or:

```bash
python3 -m retro.web_gui
```

Your browser will automatically open to `http://127.0.0.1:5000`

## ✨ Features

### Beautiful Web Interface
- 🎨 Modern gradient design
- 📱 Responsive layout
- 🌐 Works in any browser
- ⚡ Real-time updates

### Full Functionality
- 🔍 **Search Games**: Search across 49+ game systems
- 📥 **Update Database**: Fetch latest game listings
- 📚 **List Installed**: View your collection
- ⚙️ **Install Games**: One-click installation

## 🎯 Usage

### 1. Update Database
Click "Update Database" to fetch game listings from repositories.

### 2. Search for Games
Enter search terms:
- `mario` → All Mario games
- `sonic genesis` → Sonic for Genesis
- `all gba` → All GBA games
- `zelda -demo` → Zelda excluding demos

### 3. Install Games
After searching, click "Yes" when prompted to install found games.

### 4. View Collection
Click "List Installed" to see all your games.

## 🖥️ System Requirements

- **Python**: 3.7 or higher
- **RAM**: 512MB minimum
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)
- **Network**: Internet connection for downloads

## 🔧 Configuration

Settings are stored in `~/.config/retro/settings.json`:

```json
{
  "roms_dir": "~/roms",
  "fetch_workers": 10,
  "install_workers": 20
}
```

## 📝 Examples

### Search Examples

| Query | Result |
|-------|--------|
| `mario` | All Mario games |
| `mario nes` | Mario on NES only |
| `all snes` | Every SNES game |
| `sonic -demo` | Sonic, no demos |
| `zelda gba -japan` | Zelda GBA, no JP |

### Installation Flow

1. Start GUI: `retro-gui`
2. Click "Update Database"
3. Enter "sonic genesis" in search box
4. Click "Search"
5. Click "Yes" to install
6. Wait for completion

## 🌐 Why Web-Based?

We switched from tkinter to web-based GUI because:
- ✅ Works on ALL systems (Windows, macOS, Linux)
- ✅ No native GUI library issues
- ✅ Better looking and more modern
- ✅ Easier to maintain and update
- ✅ Responsive and accessible

## 🛠️ Troubleshooting

### Port Already in Use

If port 5000 is busy, edit `retro/web_gui.py`:

```python
app.run(debug=False, port=5001, host='127.0.0.1')
```

### Browser Doesn't Open

Manually visit: `http://127.0.0.1:5000`

### Can't Connect

Check firewall settings or try:
```bash
python3 -m retro.web_gui
```

Then visit `http://localhost:5000`

## 🔒 Security Note

The web server only listens on `127.0.0.1` (localhost), meaning it's NOT accessible from other computers on your network. It's completely safe to use.

## 📱 Mobile Access (Optional)

To access from mobile devices on your network:

1. Edit `retro/web_gui.py`:
   ```python
   app.run(debug=False, port=5000, host='0.0.0.0')
   ```

2. Find your computer's IP: `ifconfig` (macOS/Linux) or `ipconfig` (Windows)

3. On mobile, visit: `http://YOUR_IP:5000`

**Warning**: Only do this on trusted networks!

## 🎮 CLI Still Available

The command-line interface is still available:

```bash
retro update
retro search mario
retro install sonic genesis
retro list
```

## 📄 License

MIT License - See LICENSE file

## 🙏 Credits

Built with:
- **Flask** - Web framework
- **Python** - Core language  
- **BeautifulSoup** - HTML parsing
- **requests** - HTTP downloads

---

**Enjoy managing your retro game collection! 🎮✨**
