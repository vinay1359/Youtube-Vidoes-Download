import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from main_window import MainWindow

def main():
    """Main application entry point"""
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("YouTube Downloader")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("YouTube Downloader")
    
    # Enable high DPI scaling
    # High DPI scaling is enabled by default in PySide6; AA_EnableHighDpiScaling is not available.
    # High DPI pixmaps are enabled by default in PySide6; the following line is not necessary and can be removed.
    # app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
