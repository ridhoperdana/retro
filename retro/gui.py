try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
except ImportError:
    print("ERROR: tkinter not found!")
    print("\nPlease install tkinter:")
    print("  - Ubuntu/Debian: sudo apt install python3-tk")
    print("  - macOS: brew install python-tk")
    print("  - Windows: Included with Python installer")
    print("\nOr build a standalone executable using PyInstaller (see BUILD_INSTRUCTIONS.md)")
    import sys
    sys.exit(1)

import threading
import os
import sys

# Handle imports for both standalone and package contexts
try:
    from retro.main import Manager, Converter, RomCleaner, format_size
except ImportError:
    from main import Manager, Converter, RomCleaner, format_size

class RetroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro - Game Package Manager")
        self.root.geometry("900x700")
        
        # Variables
        self.mgr = Manager()
        self.is_loading = False
        
        # Create main layout
        self.create_menu()
        self.create_notebook()
        self.create_status_bar()
        
        # Load initial data
        self.root.after(100, self.initial_load)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Search & Install
        self.tab_search = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text="Search & Install")
        self.create_search_tab()
        
        # Tab 2: Installed Games
        self.tab_installed = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_installed, text="Installed Games")
        self.create_installed_tab()
        
        # Tab 3: Utilities
        self.tab_utils = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_utils, text="Utilities")
        self.create_utilities_tab()
    
    def create_search_tab(self):
        # Search frame
        search_frame = ttk.LabelFrame(self.tab_search, text="Search Games", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind('<Return>', lambda e: self.do_search())
        
        ttk.Button(search_frame, text="Search", command=self.do_search).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(search_frame, text="Update Database", command=self.do_update).grid(row=0, column=3, padx=5, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.tab_search, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.search_tree = ttk.Treeview(tree_frame, columns=("System", "Name", "Size", "Status"), 
                                        show="tree headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_tree.yview)
        
        self.search_tree.heading("#0", text="")
        self.search_tree.heading("System", text="System")
        self.search_tree.heading("Name", text="Name")
        self.search_tree.heading("Size", text="Size")
        self.search_tree.heading("Status", text="Status")
        
        self.search_tree.column("#0", width=30)
        self.search_tree.column("System", width=100)
        self.search_tree.column("Name", width=400)
        self.search_tree.column("Size", width=100)
        self.search_tree.column("Status", width=100)
        
        self.search_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        btn_frame = ttk.Frame(results_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Install Selected", command=self.install_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Select All", command=self.select_all_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deselect All", command=self.deselect_all_search).pack(side=tk.LEFT, padx=5)
    
    def create_installed_tab(self):
        # Control frame
        ctrl_frame = ttk.Frame(self.tab_installed)
        ctrl_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(ctrl_frame, text="Refresh", command=self.refresh_installed).pack(side=tk.LEFT, padx=5)
        
        # List frame
        list_frame = ttk.LabelFrame(self.tab_installed, text="Installed Games", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.installed_tree = ttk.Treeview(tree_frame, columns=("System", "Name", "Size"), 
                                           show="tree headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.installed_tree.yview)
        
        self.installed_tree.heading("#0", text="")
        self.installed_tree.heading("System", text="System")
        self.installed_tree.heading("Name", text="Name")
        self.installed_tree.heading("Size", text="Size")
        
        self.installed_tree.column("#0", width=30)
        self.installed_tree.column("System", width=150)
        self.installed_tree.column("Name", width=450)
        self.installed_tree.column("Size", width=100)
        
        self.installed_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Select All", command=self.select_all_installed).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deselect All", command=self.deselect_all_installed).pack(side=tk.LEFT, padx=5)
    
    def create_utilities_tab(self):
        # Compress section
        compress_frame = ttk.LabelFrame(self.tab_utils, text="Compress ROMs to CHD", padding=10)
        compress_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(compress_frame, text="Convert ISO/CUE/GDI files to compressed CHD format").pack(anchor=tk.W, pady=5)
        ttk.Button(compress_frame, text="Auto Compress All", command=self.do_compress).pack(anchor=tk.W, padx=5, pady=5)
        
        # Clean duplicates section
        clean_frame = ttk.LabelFrame(self.tab_utils, text="Remove Duplicate ROMs", padding=10)
        clean_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(clean_frame, text="Remove duplicate ROMs based on region priority (W > E > U > J)").pack(anchor=tk.W, pady=5)
        ttk.Button(clean_frame, text="Clean Duplicates", command=self.do_clean).pack(anchor=tk.W, padx=5, pady=5)
        
        # Console output
        console_frame = ttk.LabelFrame(self.tab_utils, text="Console Output", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.console = scrolledtext.ScrolledText(console_frame, height=15, state=tk.DISABLED)
        self.console.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_status(self, text):
        self.status_bar.config(text=text)
        self.root.update_idletasks()
    
    def log_console(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
    
    def initial_load(self):
        if not self.mgr.load():
            messagebox.showwarning("Warning", "Could not load systems.json. Click 'Update Database' to fetch game data.")
            return
        
        # Load initial installed games
        self.refresh_installed()
    
    def do_update(self):
        if self.is_loading:
            return
        
        def update_thread():
            self.is_loading = True
            self.set_status("Updating database...")
            try:
                self.mgr.fetch()
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Database updated! Found {len(self.mgr.files)} games."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Update failed: {str(e)}"))
            finally:
                self.is_loading = False
                self.set_status("Ready")
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def do_search(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        if not self.mgr.files:
            messagebox.showwarning("Warning", "No game data available. Click 'Update Database' first.")
            return
        
        self.set_status(f"Searching for: {query}")
        
        # Parse query
        terms = query.split()
        inc = [t.lower() for t in terms if t.lower() in [s.lower() for s in self.mgr.systems.keys()]]
        kw = [t for t in terms if t.lower() not in [s.lower() for s in self.mgr.systems.keys()] and not t.startswith('-')]
        exc = [t[1:] for t in terms if t.startswith('-')]
        
        # Search
        results = [f for f in self.mgr.files if 
                  (not inc or f["system"].lower() in inc) and 
                  (not kw or all(k.lower() in f["name"].lower() for k in kw)) and 
                  (not exc or not any(e.lower() in f["name"].lower() for e in exc))]
        
        # Clear tree
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Group by system
        by_system = {}
        for f in results:
            if f["system"] not in by_system:
                by_system[f["system"]] = []
            by_system[f["system"]].append(f)
        
        # Populate tree
        for sys_name in sorted(by_system.keys()):
            sys_files = by_system[sys_name]
            total_size = sum(f.get("size_bytes", 0) for f in sys_files)
            
            # Add system node
            sys_node = self.search_tree.insert("", tk.END, text="", 
                                              values=(sys_name, f"({len(sys_files)} games)", format_size(total_size), ""))
            
            # Add games
            for f in sys_files:
                # Check if installed
                system_dir = os.path.join(self.mgr.settings["roms_dir"], sys_name)
                is_installed = False
                if os.path.exists(system_dir):
                    bn = os.path.splitext(f["name"])[0]
                    is_installed = any(os.path.splitext(x)[0] == bn for x in os.listdir(system_dir) 
                                      if os.path.isfile(os.path.join(system_dir, x)))
                
                status = "Installed" if is_installed else ""
                self.search_tree.insert(sys_node, tk.END, text="☐", 
                                       values=("", f["name"], format_size(f.get("size_bytes", 0)), status),
                                       tags=("game",))
        
        self.set_status(f"Found {len(results)} games")
    
    def refresh_installed(self):
        if not self.mgr.load():
            return
        
        self.set_status("Loading installed games...")
        
        # Clear tree
        for item in self.installed_tree.get_children():
            self.installed_tree.delete(item)
        
        # Get installed games
        all_files = []
        for sys_name in self.mgr.systems:
            system_dir = os.path.join(self.mgr.settings["roms_dir"], sys_name)
            if not os.path.exists(system_dir):
                continue
            for file in os.listdir(system_dir):
                file_path = os.path.join(system_dir, file)
                if os.path.isfile(file_path) and not file.startswith('.'):
                    all_files.append({"name": file, "path": file_path, "system": sys_name})
        
        # Group by system
        by_system = {}
        for f in all_files:
            if f["system"] not in by_system:
                by_system[f["system"]] = []
            by_system[f["system"]].append(f)
        
        # Populate tree
        total_games = 0
        for sys_name in sorted(by_system.keys()):
            sys_files = by_system[sys_name]
            total_size = sum(os.path.getsize(f['path']) for f in sys_files)
            
            # Add system node
            sys_node = self.installed_tree.insert("", tk.END, text="",
                                                  values=(sys_name, f"({len(sys_files)} games)", format_size(total_size)))
            
            # Add games
            for f in sys_files:
                self.installed_tree.insert(sys_node, tk.END, text="☐",
                                          values=("", f["name"], format_size(os.path.getsize(f['path']))),
                                          tags=("game",))
                total_games += 1
        
        self.set_status(f"Loaded {total_games} installed games")
    
    def get_selected_items(self, tree):
        selected = []
        for item in tree.get_children():
            for child in tree.get_children(item):
                if tree.item(child)["text"] == "☑":
                    selected.append(child)
        return selected
    
    def install_selected(self):
        selected = self.get_selected_items(self.search_tree)
        if not selected:
            messagebox.showwarning("Warning", "No games selected")
            return
        
        # Get package info
        packages = []
        for item in selected:
            values = self.search_tree.item(item)["values"]
            name = values[1]
            
            # Find in mgr.files
            for f in self.mgr.files:
                if f["name"] == name:
                    packages.append(f)
                    break
        
        if not packages:
            return
        
        # Confirm
        total_size = sum(f.get("size_bytes", 0) for f in packages)
        if not messagebox.askyesno("Confirm", f"Install {len(packages)} games ({format_size(total_size)})?"):
            return
        
        # Install in thread
        def install_thread():
            self.set_status(f"Installing {len(packages)} games...")
            try:
                self.mgr.install(packages)
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Installed {len(packages)} games!"))
                self.root.after(0, self.refresh_installed)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Installation failed: {str(e)}"))
            finally:
                self.set_status("Ready")
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def remove_selected(self):
        selected = self.get_selected_items(self.installed_tree)
        if not selected:
            messagebox.showwarning("Warning", "No games selected")
            return
        
        # Get file paths
        files = []
        for item in selected:
            values = self.installed_tree.item(item)["values"]
            name = values[1]
            parent = self.installed_tree.parent(item)
            system = self.installed_tree.item(parent)["values"][0]
            path = os.path.join(self.mgr.settings["roms_dir"], system, name)
            files.append(path)
        
        # Confirm
        total_size = sum(os.path.getsize(f) for f in files if os.path.exists(f))
        if not messagebox.askyesno("Confirm", f"Remove {len(files)} games ({format_size(total_size)})?"):
            return
        
        # Remove
        for f in files:
            if os.path.exists(f):
                os.remove(f)
        
        messagebox.showinfo("Success", f"Removed {len(files)} games!")
        self.refresh_installed()
    
    def select_all_search(self):
        self.toggle_all(self.search_tree, True)
    
    def deselect_all_search(self):
        self.toggle_all(self.search_tree, False)
    
    def select_all_installed(self):
        self.toggle_all(self.installed_tree, True)
    
    def deselect_all_installed(self):
        self.toggle_all(self.installed_tree, False)
    
    def toggle_all(self, tree, select):
        for item in tree.get_children():
            for child in tree.get_children(item):
                tree.item(child, text="☑" if select else "☐")
    
    # Toggle checkbox on click
    def toggle_checkbox(self, tree):
        def handler(event):
            item = tree.identify('item', event.x, event.y)
            if item and "game" in tree.item(item, "tags"):
                current = tree.item(item)["text"]
                tree.item(item, text="☑" if current == "☐" else "☐")
        return handler
    
    def __init__(self, root):
        self.root = root
        self.root.title("Retro - Game Package Manager")
        self.root.geometry("900x700")
        
        # Variables
        self.mgr = Manager()
        self.is_loading = False
        
        # Create main layout
        self.create_menu()
        self.create_notebook()
        self.create_status_bar()
        
        # Bind checkbox toggle
        self.root.after(100, lambda: self.search_tree.bind('<Button-1>', self.toggle_checkbox(self.search_tree)))
        self.root.after(100, lambda: self.installed_tree.bind('<Button-1>', self.toggle_checkbox(self.installed_tree)))
        
        # Load initial data
        self.root.after(100, self.initial_load)
    
    def do_compress(self):
        if not messagebox.askyesno("Confirm", "This will compress all ISO/CUE/GDI files to CHD format. Continue?"):
            return
        
        def compress_thread():
            self.set_status("Compressing ROMs...")
            try:
                converter = Converter()
                converter.auto_compress_all()
                self.root.after(0, lambda: messagebox.showinfo("Success", "Compression complete!"))
                self.root.after(0, self.refresh_installed)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Compression failed: {str(e)}"))
            finally:
                self.set_status("Ready")
        
        threading.Thread(target=compress_thread, daemon=True).start()
    
    def do_clean(self):
        if not messagebox.askyesno("Confirm", "This will remove duplicate ROMs based on region priority. Continue?"):
            return
        
        def clean_thread():
            self.set_status("Cleaning duplicates...")
            try:
                cleaner = RomCleaner("W,E,U,J")
                cleaner.clean()
                self.root.after(0, lambda: messagebox.showinfo("Success", "Duplicate cleaning complete!"))
                self.root.after(0, self.refresh_installed)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Cleaning failed: {str(e)}"))
            finally:
                self.set_status("Ready")
        
        threading.Thread(target=clean_thread, daemon=True).start()
    
    def show_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("500x300")
        
        ttk.Label(settings_win, text="ROMs Directory:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        roms_dir = ttk.Entry(settings_win, width=40)
        roms_dir.insert(0, self.mgr.settings["roms_dir"])
        roms_dir.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(settings_win, text="Fetch Workers:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        fetch_workers = ttk.Entry(settings_win, width=10)
        fetch_workers.insert(0, str(self.mgr.settings["fetch_workers"]))
        fetch_workers.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(settings_win, text="Install Workers:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        install_workers = ttk.Entry(settings_win, width=10)
        install_workers.insert(0, str(self.mgr.settings["install_workers"]))
        install_workers.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        def save_settings():
            import json
            settings = {
                "roms_dir": roms_dir.get(),
                "fetch_workers": int(fetch_workers.get()),
                "install_workers": int(install_workers.get()),
                "convert_workers": self.mgr.settings["convert_workers"],
                "compress_workers": self.mgr.settings["compress_workers"]
            }
            settings_file = os.path.join(self.mgr.config_dir, "settings.json")
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved!")
            settings_win.destroy()
        
        ttk.Button(settings_win, text="Save", command=save_settings).grid(row=3, column=0, columnspan=2, pady=20)
    
    def show_about(self):
        messagebox.showinfo("About", "Retro - Game Package Manager\nVersion 1.0.0\n\nA tool for managing retro game collections.")


def main():
    root = tk.Tk()
    app = RetroGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

