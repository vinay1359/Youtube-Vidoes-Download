#!/usr/bin/env python3
"""
YouTube Downloader GUI Launcher
Run this file to start the desktop application
"""

import sys
import os

# Add the gui directory to Python path
gui_path = os.path.join(os.path.dirname(__file__), 'gui')
sys.path.insert(0, gui_path)

# Import and run the application
from gui.app import main

if __name__ == "__main__":
    main()