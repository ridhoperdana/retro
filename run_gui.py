#!/usr/bin/env python3
"""
Entry point for Retro GUI application.
This file is used by PyInstaller to build the standalone executable.
"""

import sys
import os

# Add the parent directory to the path so we can import retro package
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# Now import and run the GUI
from retro.gui import main

if __name__ == "__main__":
    main()

