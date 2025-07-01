import os
import subprocess
import shutil
import platform
import hashlib

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
OUTPUT_FOLDER = os.path.join(DESKTOP_PATH, "YouTube Videos")
DOWNLOAD_HISTORY_FILE = os.path.join(OUTPUT_FOLDER, ".download_history.txt")

# Detect yt-dlp path or use a manually defined path
YT_DLP_PATH = shutil.which("yt-dlp")
if not YT_DLP_PATH:
    # Try common installation paths
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

def get_downloaded_video_ids():
    """Read the history file to get previously downloaded video IDs"""
    if not os.path.exists(DOWNLOAD_HISTORY_FILE):
        return set()
    
    with open(DOWNLOAD_HISTORY_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def add_video_to_history(video_id):
    """Add a video ID to the download history"""
    with open(DOWNLOAD_HISTORY_FILE, 'a') as f:
        f.write(f"{video_id}\n")

def download_videos(url):
    """Download videos from URL (works with single videos or playlists)"""
    # First, get video IDs without downloading
    print("Checking for videos to download...")
    info_command = [
        YT_DLP_PATH,
        "--flat-playlist",
        "--get-id",
        url
    ]
    
    result = subprocess.run(info_command, capture_output=True, text=True)
    video_ids = result.stdout.strip().split('\n')
    video_ids = [vid for vid in video_ids if vid.strip()]  # Filter out empty lines
    
    # Get already downloaded videos
    downloaded_ids = get_downloaded_video_ids()
    
    # Filter out videos that have already been downloaded
    new_videos = [vid for vid in video_ids if vid not in downloaded_ids]
    
    if not new_videos:
        print("Already video downloaded, so dont download!")
        return
    
    print(f"Found {len(new_videos)} new video(s) to download")
    
    # Download new videos
    for video_id in new_videos:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading video ID: {video_id}")
        
        command = [
            YT_DLP_PATH,
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "--output", os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s"),
            "--sleep-interval", "3",
            "--limit-rate", "2M",
            video_url
        ]
        
        subprocess.run(command)
        
        # Add to download history
        add_video_to_history(video_id)
        print(f"Video {video_id} downloaded and added to history")

def main():
    print("YouTube Video Downloader")
    print("=" * 50)
    print(f"Videos will be saved to: {OUTPUT_FOLDER}")
    
    url = input("Enter YouTube URL (video or playlist): ")
    
    if not url.strip():
        print("No URL provided. Exiting.")
        return
    
    print("\nStarting download process...")
    download_videos(url)
    print("\nDownload process completed!")

if __name__ == "__main__":
    main()