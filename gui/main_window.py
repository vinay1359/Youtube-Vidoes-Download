import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QTabWidget, QFrame, QProgressBar,
                            QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QThread, Signal as pyqtSignal, QTimer
from PySide6.QtGui import QFont, QIcon, QPalette, QColor
# Make sure download_worker.py exists in the same directory as this file.
# If it's in a subfolder (e.g., 'workers'), use: from workers.download_worker import DownloadWorker
from download_worker import DownloadWorker
import platform

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(700, 500)
        
        # Set application style
        self.setStyleSheet(self.get_stylesheet())
        
        # Initialize UI
        self.init_ui()
        
        # Download worker thread
        self.download_worker = None
        
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("YouTube Downloader")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tabWidget")
        
        # Video download tab
        video_tab = self.create_video_tab()
        self.tab_widget.addTab(video_tab, "📹 Video Download")
        
        # Audio download tab
        audio_tab = self.create_audio_tab()
        self.tab_widget.addTab(audio_tab, "🎵 Audio Download")
        
        main_layout.addWidget(self.tab_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progressBar")
        main_layout.addWidget(self.progress_bar)
        
        # Status/Output area
        self.output_text = QTextEdit()
        self.output_text.setObjectName("outputText")
        self.output_text.setMaximumHeight(200)
        self.output_text.setPlaceholderText("Download status and messages will appear here...")
        main_layout.addWidget(self.output_text)
        
    def create_video_tab(self):
        """Create the video download tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # URL input section
        url_frame = QFrame()
        url_frame.setObjectName("inputFrame")
        url_layout = QVBoxLayout(url_frame)
        
        url_label = QLabel("Enter YouTube URL (Video or Playlist):")
        url_label.setObjectName("inputLabel")
        url_layout.addWidget(url_label)
        
        self.video_url_input = QLineEdit()
        self.video_url_input.setObjectName("urlInput")
        self.video_url_input.setPlaceholderText("https://www.youtube.com/watch?v=... or https://www.youtube.com/playlist?list=...")
        url_layout.addWidget(self.video_url_input)
        
        layout.addWidget(url_frame)
        
        # Buttons section
        button_layout = QHBoxLayout()
        
        self.video_download_btn = QPushButton("📥 Download Videos")
        self.video_download_btn.setObjectName("downloadButton")
        self.video_download_btn.clicked.connect(self.start_video_download)
        
        self.video_open_folder_btn = QPushButton("📁 Open Videos Folder")
        self.video_open_folder_btn.setObjectName("folderButton")
        self.video_open_folder_btn.clicked.connect(self.open_videos_folder)
        
        button_layout.addWidget(self.video_download_btn)
        button_layout.addWidget(self.video_open_folder_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Info section
        info_label = QLabel("Videos will be saved to: Desktop/YouTube Videos")
        info_label.setObjectName("infoLabel")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return tab
        
    def create_audio_tab(self):
        """Create the audio download tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # URL input section
        url_frame = QFrame()
        url_frame.setObjectName("inputFrame")
        url_layout = QVBoxLayout(url_frame)
        
        url_label = QLabel("Enter YouTube URL (Video or Playlist):")
        url_label.setObjectName("inputLabel")
        url_layout.addWidget(url_label)
        
        self.audio_url_input = QLineEdit()
        self.audio_url_input.setObjectName("urlInput")
        self.audio_url_input.setPlaceholderText("https://www.youtube.com/watch?v=... or https://www.youtube.com/playlist?list=...")
        url_layout.addWidget(self.audio_url_input)
        
        layout.addWidget(url_frame)
        
        # Buttons section
        button_layout = QHBoxLayout()
        
        self.audio_download_btn = QPushButton("🎵 Download Audio")
        self.audio_download_btn.setObjectName("downloadButton")
        self.audio_download_btn.clicked.connect(self.start_audio_download)
        
        self.audio_open_folder_btn = QPushButton("📁 Open Audio Folder")
        self.audio_open_folder_btn.setObjectName("folderButton")
        self.audio_open_folder_btn.clicked.connect(self.open_audio_folder)
        
        button_layout.addWidget(self.audio_download_btn)
        button_layout.addWidget(self.audio_open_folder_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Info section
        info_label = QLabel("Audio files (MP3 with thumbnails) will be saved to: Desktop/YouTube Audio")
        info_label.setObjectName("infoLabel")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return tab
        
    def start_video_download(self):
        """Start video download process"""
        url = self.video_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a YouTube URL")
            return
            
        self.start_download(url, "video")
        
    def start_audio_download(self):
        """Start audio download process"""
        url = self.audio_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a YouTube URL")
            return
            
        self.start_download(url, "audio")
        
    def start_download(self, url, download_type):
        """Start the download process in a separate thread"""
        if self.download_worker and self.download_worker.isRunning():
            QMessageBox.information(self, "Info", "A download is already in progress. Please wait...")
            return
            
        # Clear output and show progress
        self.output_text.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Disable download buttons
        self.video_download_btn.setEnabled(False)
        self.audio_download_btn.setEnabled(False)
        
        # Create and start worker thread
        self.download_worker = DownloadWorker(url, download_type)
        self.download_worker.output_signal.connect(self.update_output)
        self.download_worker.finished_signal.connect(self.download_finished)
        self.download_worker.error_signal.connect(self.download_error)
        self.download_worker.start()
        
    def update_output(self, text):
        """Update the output text area"""
        self.output_text.append(text)
        scroll_bar = self.output_text.verticalScrollBar()
        if scroll_bar is not None:
            scroll_bar.setValue(scroll_bar.maximum())
        
    def download_finished(self, success, message):
        """Handle download completion"""
        self.progress_bar.setVisible(False)
        self.video_download_btn.setEnabled(True)
        self.audio_download_btn.setEnabled(True)
        
        if success:
            self.update_output(f"✅ {message}")
            QMessageBox.information(self, "Success", message)
        else:
            self.update_output(f"❌ {message}")
            QMessageBox.warning(self, "Download Failed", message)
            
    def download_error(self, error_message):
        """Handle download errors"""
        self.progress_bar.setVisible(False)
        self.video_download_btn.setEnabled(True)
        self.audio_download_btn.setEnabled(True)
        
        self.update_output(f"❌ Error: {error_message}")
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")
        
    def open_videos_folder(self):
        """Open the videos download folder"""
        desktop_path = self.get_desktop_path()
        folder_path = os.path.join(desktop_path, "YouTube Videos")
        self.open_folder(folder_path)
        
    def open_audio_folder(self):
        """Open the audio download folder"""
        desktop_path = self.get_desktop_path()
        folder_path = os.path.join(desktop_path, "YouTube Audio")
        self.open_folder(folder_path)
        
    def open_folder(self, folder_path):
        """Open folder in file explorer"""
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                os.system(f"open '{folder_path}'")
            else:  # Linux
                os.system(f"xdg-open '{folder_path}'")
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open folder: {str(e)}")
            
    def get_desktop_path(self):
        """Get the desktop path based on the operating system"""
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        elif platform.system() == "Darwin":  # macOS
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:  # Linux and other Unix-like systems
            return os.path.join(os.path.expanduser("~"), "Desktop")
            
    def get_stylesheet(self):
        """Return the application stylesheet"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        #title {
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin: 20px 0;
        }
        
        #tabWidget {
            background-color: white;
            border-radius: 10px;
        }
        
        QTabWidget::pane {
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: white;
        }
        
        QTabWidget::tab-bar {
            alignment: center;
        }
        
        QTabBar::tab {
            background-color: #ecf0f1;
            color: #2c3e50;
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: bold;
        }
        
        QTabBar::tab:selected {
            background-color: #3498db;
            color: white;
        }
        
        QTabBar::tab:hover {
            background-color: #bdc3c7;
        }
        
        #inputFrame {
            background-color: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
        }
        
        #inputLabel {
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
        }
        
        #urlInput {
            padding: 12px;
            font-size: 14px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
        }
        
        #urlInput:focus {
            border-color: #3498db;
            background-color: white;
        }
        
        #downloadButton {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 15px 25px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            min-width: 150px;
        }
        
        #downloadButton:hover {
            background-color: #229954;
        }
        
        #downloadButton:pressed {
            background-color: #1e8449;
        }
        
        #downloadButton:disabled {
            background-color: #95a5a6;
        }
        
        #folderButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 15px 25px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            min-width: 150px;
        }
        
        #folderButton:hover {
            background-color: #2980b9;
        }
        
        #folderButton:pressed {
            background-color: #21618c;
        }
        
        #infoLabel {
            color: #7f8c8d;
            font-size: 12px;
            font-style: italic;
        }
        
        #progressBar {
            height: 8px;
            border-radius: 4px;
            background-color: #ecf0f1;
        }
        
        #progressBar::chunk {
            background-color: #3498db;
            border-radius: 4px;
        }
        
        #outputText {
            background-color: #2c3e50;
            color: #ecf0f1;
            border: 1px solid #34495e;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
        }
        """