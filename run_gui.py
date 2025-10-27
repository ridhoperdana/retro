#!/usr/bin/env python3
"""
Entry point for Retro Web GUI application.
"""

import sys
import os

# Add the parent directory to the path
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# Import and run the Web GUI
from retro.web_gui import main

if __name__ == "__main__":
    main()
