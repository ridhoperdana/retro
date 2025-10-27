"""Web-based GUI for Retro - Works on any system!"""

from flask import Flask, render_template_string, request, jsonify
import webbrowser
import threading
import os

try:
    from retro.main import Manager, format_size
except ImportError:
    from main import Manager, format_size

app = Flask(__name__)
mgr = Manager()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Retro Game Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .content { padding: 30px; }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        input[type="text"] {
            flex: 1;
            min-width: 300px;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
        }
        button {
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover { background: #5568d3; transform: translateY(-2px); }
        .btn-success {
            background: #27ae60;
            color: white;
        }
        .btn-success:hover { background: #229954; transform: translateY(-2px); }
        .btn-info {
            background: #3498db;
            color: white;
        }
        .btn-info:hover { background: #2980b9; transform: translateY(-2px); }
        #output {
            background: #f8f9fa;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            line-height: 1.6;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .status-bar {
            background: #2c3e50;
            color: white;
            padding: 15px 30px;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 Retro Game Manager</h1>
            <p>Search, Download, and Manage Retro Games</p>
        </div>
        
        <div class="content">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Enter search terms (e.g., 'mario', 'sonic genesis', 'all gba')">
                <button class="btn-primary" onclick="search()">Search</button>
                <button class="btn-success" onclick="updateDB()">Update Database</button>
                <button class="btn-info" onclick="listInstalled()">List Installed</button>
            </div>
            
            <div id="output">
Welcome to Retro Game Manager!

1. Click "Update Database" to fetch game listings
2. Enter search terms and click "Search"
3. Follow instructions to install games

Examples:
  • "mario" → All Mario games
  • "sonic genesis" → Sonic games for Genesis
  • "all gba" → All Game Boy Advance games
            </div>
        </div>
        
        <div class="status-bar" id="status">Ready</div>
    </div>
    
    <script>
        function log(text) {
            document.getElementById('output').textContent += '\\n' + text;
            document.getElementById('output').scrollTop = document.getElementById('output').scrollHeight;
        }
        
        function setStatus(text) {
            document.getElementById('status').textContent = text;
        }
        
        function showLoading() {
            document.getElementById('output').innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading...</p></div>';
        }
        
        async function updateDB() {
            setStatus('Updating database...');
            showLoading();
            try {
                const res = await fetch('/api/update');
                const data = await res.json();
                document.getElementById('output').textContent = data.output;
                setStatus(data.status);
            } catch(e) {
                log('Error: ' + e);
                setStatus('Error');
            }
        }
        
        async function search() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) {
                alert('Please enter search terms');
                return;
            }
            setStatus('Searching...');
            showLoading();
            try {
                const res = await fetch('/api/search?q=' + encodeURIComponent(query));
                const data = await res.json();
                document.getElementById('output').textContent = data.output;
                setStatus(data.status);
                
                if (data.count > 0 && confirm(`Install ${data.count} games?`)) {
                    await install(query);
                }
            } catch(e) {
                log('Error: ' + e);
                setStatus('Error');
            }
        }
        
        async function install(query) {
            setStatus('Installing...');
            showLoading();
            try {
                const res = await fetch('/api/install?q=' + encodeURIComponent(query));
                const data = await res.json();
                document.getElementById('output').textContent = data.output;
                setStatus(data.status);
            } catch(e) {
                log('Error: ' + e);
                setStatus('Error');
            }
        }
        
        async function listInstalled() {
            setStatus('Loading...');
            showLoading();
            try {
                const res = await fetch('/api/list');
                const data = await res.json();
                document.getElementById('output').textContent = data.output;
                setStatus(data.status);
            } catch(e) {
                log('Error: ' + e);
                setStatus('Error');
            }
        }
        
        // Enter key to search
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') search();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

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

def main():
    print("🎮 Starting Retro Game Manager Web GUI...")
    print("📡 Server will start at: http://127.0.0.1:5000")
    print("🌐 Opening browser...")
    print("\n⚠️  If browser doesn't open, manually visit: http://127.0.0.1:5000")
    print("⏹️  Press CTRL+C to stop the server\n")
    
    # Open browser after short delay
    threading.Timer(1.5, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    
    # Start Flask with explicit host
    app.run(debug=False, port=5000, host='127.0.0.1', threaded=True)

if __name__ == '__main__':
    main()

