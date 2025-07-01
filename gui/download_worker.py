import sys
import os
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadWorker(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, url, download_type):
        super().__init__()
        self.url = url
        self.download_type = download_type
        
    def run(self):
        """Run the download process"""
        try:
            # Determine which backend script to run
            if self.download_type == "video":
                script_path = os.path.join("downloadall", "video.py")
                success_message = "Video download completed successfully!"
            else:  # audio
                script_path = os.path.join("downloadall", "audio_only.py")
                success_message = "Audio download completed successfully!"
            
            # Check if script exists
            if not os.path.exists(script_path):
                self.error_signal.emit(f"Backend script not found: {script_path}")
                return
                
            self.output_signal.emit(f"Starting {self.download_type} download...")
            self.output_signal.emit(f"URL: {self.url}")
            self.output_signal.emit("-" * 50)
            
            # Create process to run the backend script
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Send URL to the script, if stdin is available
            if process.stdin:
                process.stdin.write(self.url + '\n')
                process.stdin.flush()
                process.stdin.close()
            else:
                self.error_signal.emit("Failed to open stdin for the subprocess.")
                return
            
            # Read output line by line
            if process.stdout is not None:
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.output_signal.emit(output.strip())
            else:
                self.error_signal.emit("Failed to open stdout for the subprocess.")
                return
            
            # Wait for process to complete
            return_code = process.wait()
            
            if return_code == 0:
                self.finished_signal.emit(True, success_message)
            else:
                self.finished_signal.emit(False, f"Download failed with return code: {return_code}")
                
        except Exception as e:
            self.error_signal.emit(str(e))