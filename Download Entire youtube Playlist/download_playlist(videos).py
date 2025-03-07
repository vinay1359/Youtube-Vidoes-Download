import os
import subprocess
import shutil

# Detect yt-dlp path or use a manually defined path
YT_DLP_PATH = shutil.which("yt-dlp")
if not YT_DLP_PATH:
    YT_DLP_PATH = r"C:\Users\bhara\Desktop\yt-dlp.exe"
    if not os.path.exists(YT_DLP_PATH):
        print("Error: yt-dlp not found. Install it using: pip install yt-dlp")
        exit(1)

def download_playlist(playlist_url, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    command = [
        YT_DLP_PATH,
        "-f", "bestvideo+bestaudio/best",  # Download best available quality
        "--merge-output-format", "mp4",   # Merge video and audio into MP4 format
        "--output", os.path.join(output_folder, "%(title)s.%(ext)s"),  # Save with video title
        "--sleep-interval", "5",          # Wait 5 seconds between downloads to avoid rate limiting
        "--limit-rate", "1M",             # Limit download speed to 1MB/s
        "--no-warnings",                  # Suppress warnings
        playlist_url
    ]

    subprocess.run(command)  # Execute yt-dlp command

playlist_url = input("Enter YouTube Playlist URL: ")
output_folder = r"C:\Users\bhara\Desktop\songs"

download_playlist(playlist_url, output_folder)
