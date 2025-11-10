"""Web-based GUI for Retro - Works on any system!"""

from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import argparse
import os

try:
    from retro.main import Manager, format_size
except ImportError:
    from main import Manager, format_size

app = Flask(__name__)
mgr = Manager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Tauri app to verify backend is ready"""
    return jsonify({'status': 'ok', 'message': 'Backend is ready'})

@app.route('/api/update')
def api_update():
    try:
        mgr.fetch()
        output = f"✅ Success! Found {len(mgr.files)} games across {len(mgr.systems)} systems"
        return jsonify({'output': output, 'status': 'Ready', 'count': len(mgr.files)})
    except Exception as e:
        return jsonify({'output': f"❌ Error: {str(e)}", 'status': 'Error', 'count': 0})

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'output': 'No query provided', 'status': 'Error', 'count': 0})
    
    if not mgr.files:
        return jsonify({'output': 'No data. Click "Update Database" first.', 'status': 'Error', 'count': 0})
    
    # Parse and search
    terms = query.split()
    inc = [t.lower() for t in terms if t.lower() in [s.lower() for s in mgr.systems.keys()]]
    kw = [t for t in terms if t.lower() not in [s.lower() for s in mgr.systems.keys()] and not t.startswith('-')]
    exc = [t[1:] for t in terms if t.startswith('-')]
    
    results = [f for f in mgr.files if 
              (not inc or f["system"].lower() in inc) and 
              (not kw or all(k.lower() in f["name"].lower() for k in kw)) and 
              (not exc or not any(e.lower() in f["name"].lower() for e in exc))]
    
    if not results:
        return jsonify({'output': 'No games found', 'status': 'Ready', 'count': 0})
    
    # Format output
    by_system = {}
    for f in results:
        if f["system"] not in by_system:
            by_system[f["system"]] = []
        by_system[f["system"]].append(f)
    
    output = f"Found {len(results)} games:\n" + "="*60 + "\n\n"
    for sys_name in sorted(by_system.keys()):
        files = by_system[sys_name]
        total = sum(f.get("size_bytes", 0) for f in files)
        output += f"[{sys_name}] {format_size(total)} ({len(files)} games)\n"
        for f in files[:20]:
            output += f"  • {f['name']} ({format_size(f.get('size_bytes', 0))})\n"
        if len(files) > 20:
            output += f"  ... and {len(files) - 20} more\n"
        output += "\n"
    
    return jsonify({'output': output, 'status': f'Found {len(results)} games', 'count': len(results), 'results': results})

@app.route('/api/install')
def api_install():
    query = request.args.get('q', '')
    # Re-do search to get packages
    terms = query.split()
    inc = [t.lower() for t in terms if t.lower() in [s.lower() for s in mgr.systems.keys()]]
    kw = [t for t in terms if t.lower() not in [s.lower() for s in mgr.systems.keys()] and not t.startswith('-')]
    exc = [t[1:] for t in terms if t.startswith('-')]
    
    results = [f for f in mgr.files if 
              (not inc or f["system"].lower() in inc) and 
              (not kw or all(k.lower() in f["name"].lower() for k in kw)) and 
              (not exc or not any(e.lower() in f["name"].lower() for e in exc))]
    
    try:
        mgr.install(results)
        output = f"✅ Successfully installed {len(results)} games!"
        return jsonify({'output': output, 'status': 'Ready'})
    except Exception as e:
        return jsonify({'output': f"❌ Error: {str(e)}", 'status': 'Error'})

@app.route('/api/list')
def api_list():
    if not mgr.load():
        return jsonify({'output': 'Could not load systems', 'status': 'Error'})
    
    output = "📚 Installed Games:\n" + "="*60 + "\n\n"
    total_files = 0
    total_size = 0
    
    for sys_name in sorted(mgr.systems.keys()):
        sys_dir = os.path.join(mgr.settings["roms_dir"], sys_name)
        if not os.path.exists(sys_dir):
            continue
        
        files = [f for f in os.listdir(sys_dir) 
                if os.path.isfile(os.path.join(sys_dir, f)) and not f.startswith('.')]
        
        if files:
            sys_size = sum(os.path.getsize(os.path.join(sys_dir, f)) for f in files)
            output += f"[{sys_name}] {format_size(sys_size)} ({len(files)} games)\n"
            for f in files[:20]:
                size = os.path.getsize(os.path.join(sys_dir, f))
                output += f"  • {f} ({format_size(size)})\n"
            if len(files) > 20:
                output += f"  ... and {len(files) - 20} more\n"
            output += "\n"
            
            total_files += len(files)
            total_size += sys_size
    
    if total_files == 0:
        output += "No games installed yet\n"
    else:
        output += "="*60 + "\n"
        output += f"Total: {format_size(total_size)} ({total_files} games)\n"
    
    return jsonify({'output': output, 'status': f'{total_files} games installed'})

def main(host: str = '127.0.0.1', port: int = 5001, open_browser: bool = True):
    url = f"http://{host}:{port}"
    print("🎮 Starting Retro Game Manager Web GUI...")
    print(f"📡 Server will start at: {url}")
    if open_browser:
        print("🌐 Opening browser...")
    print(f"\n⚠️  If browser doesn't open, manually visit: {url}")
    print("⏹️  Press CTRL+C to stop the server\n")
    
    # Open browser after short delay
    if open_browser and os.environ.get("RETRO_GUI_NO_BROWSER", "").lower() not in {"1", "true", "yes"}:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    
    # Start Flask with explicit host
    app.run(debug=False, port=port, host=host, threaded=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Retro Game Manager web GUI.")
    parser.add_argument("--host", default="127.0.0.1", help="Host address to bind the server.")
    parser.add_argument("--port", type=int, default=5001, help="Port for the web server.")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser.")
    args = parser.parse_args()
    main(host=args.host, port=args.port, open_browser=not args.no_browser)
