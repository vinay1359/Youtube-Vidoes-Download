import os
import subprocess
import shutil
import platform

# Determine user's desktop path based on the operating system
def get_desktop_path():
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:  # Linux and other Unix-like systems
        return os.path.join(os.path.expanduser("~"), "Desktop")

# Setup paths
DESKTOP_PATH = get_desktop_path()
OUTPUT_FOLDER = os.path.join(DESKTOP_PATH, "YouTube Audio")
DOWNLOAD_HISTORY_FILE = os.path.join(OUTPUT_FOLDER, ".audio_download_history.txt")

# Detect yt-dlp path
YT_DLP_PATH = shutil.which("yt-dlp")
if not YT_DLP_PATH:
    possible_paths = [
        r"C:\Users\bhara\Desktop\yt-dlp.exe",
        os.path.join(os.path.expanduser("~"), "yt-dlp"),
        os.path.join(os.path.expanduser("~"), "yt-dlp.exe"),
        "./yt-dlp",
        "./yt-dlp.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            YT_DLP_PATH = path
            break
    
    if not YT_DLP_PATH:
        print("Error: yt-dlp not found. Install it using: pip install yt-dlp")
        exit(1)

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Create download history file if it doesn't exist
if not os.path.exists(DOWNLOAD_HISTORY_FILE):
    with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
        pass

def get_downloaded_audio_ids():
    """Read the history file to get previously downloaded audio IDs"""
    if not os.path.exists(DOWNLOAD_HISTORY_FILE):
        return set()
    
    with open(DOWNLOAD_HISTORY_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def add_audio_to_history(video_id):
    """Add a video ID to the download history after audio extraction"""
    with open(DOWNLOAD_HISTORY_FILE, 'a') as f:
        f.write(f"{video_id}\n")

def download_audio(url):
    """Download audio from URL with embedded thumbnail"""
    # Get video IDs without downloading
    print("Checking for audio to download...")
    info_command = [
        YT_DLP_PATH,
        "--flat-playlist",
        "--get-id",
        url
    ]
    
    result = subprocess.run(info_command, capture_output=True, text=True)
    video_ids = result.stdout.strip().split('\n')
    video_ids = [vid for vid in video_ids if vid.strip()]  # Filter out empty lines
    
    # Get already downloaded audios
    downloaded_ids = get_downloaded_audio_ids()
    
    # Filter out videos that have already been downloaded
    new_videos = [vid for vid in video_ids if vid not in downloaded_ids]
    
    if not new_videos:
        print("already audio download, so dont download!")
        return
    
    print(f"Found {len(new_videos)} new audio track(s) to download")
    
    # Download new audio
    for video_id in new_videos:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading audio from video ID: {video_id}")
        
        # Use yt-dlp's built-in thumbnail embedding
        command = [
            YT_DLP_PATH,
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",  # This is the key flag to embed thumbnails
            "--convert-thumbnails", "jpg",
            "--output", os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s"),
            "--sleep-interval", "2",
            video_url
        ]
        
        result = subprocess.run(command)
        
        if result.returncode == 0:
            # Add to download history
            add_audio_to_history(video_id)
            print(f"Audio from video {video_id} downloaded with thumbnail")
        else:
            print(f"Error downloading audio for {video_id}")

def main():
    print("YouTube Audio Downloader with Thumbnails")
    print("=" * 50)
    print(f"Audio files will be saved to: {OUTPUT_FOLDER}")
    
    url = input("Enter YouTube URL (video or playlist): ")
    
    if not url.strip():
        print("No URL provided. Exiting.")
        return
    
    print("\nStarting audio download process...")
    download_audio(url)
    print("\nAudio download process completed!")

if __name__ == "__main__":
    main()