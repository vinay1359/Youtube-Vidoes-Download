import os
import subprocess
import shutil
import time

# Detect yt-dlp and ffmpeg paths
YT_DLP_PATH = shutil.which("yt-dlp")
FFMPEG_PATH = shutil.which("ffmpeg")

# If yt-dlp is not found, check the manual path
if not YT_DLP_PATH:
    YT_DLP_PATH = r"C:\Users\bhara\Desktop\yt-dlp.exe"
    if not os.path.exists(YT_DLP_PATH):
        print("Error: yt-dlp not found. Install it using: pip install yt-dlp")
        exit(1)

# If ffmpeg is not found, exit with an error
if not FFMPEG_PATH:
    print("Error: ffmpeg not found. Install it from https://ffmpeg.org/download.html")
    exit(1)

def download_audio_with_cover(playlist_url, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the list of video URLs from the playlist
    command = [YT_DLP_PATH, "--flat-playlist", "--print", "%(url)s", playlist_url]
    result = subprocess.run(command, capture_output=True, text=True)
    video_urls = result.stdout.strip().split("\n")  # Extract video URLs

    # Loop through each video URL and download audio
    for index, video_url in enumerate(video_urls, start=1):
        print(f"\n🔹 Downloading {index}/{len(video_urls)}: {video_url}")

        command = [
            YT_DLP_PATH,
            "-f", "bestaudio",  # Select the best audio format available
            "--extract-audio",  # Extract audio only
            "--audio-format", "mp3",  # Convert to MP3 format
            "--audio-quality", "0",  # Highest audio quality
            "--output", os.path.join(output_folder, "%(title)s.%(ext)s"),  # Save with video title
            "--write-thumbnail",  # Download thumbnail as a cover image
            "--sleep-interval", "2",  # Wait 2 seconds between downloads to avoid rate limiting
            "--limit-rate", "1M",  # Limit download speed to prevent getting blocked
            "--no-warnings",  # Suppress warnings
            video_url
        ]

        subprocess.run(command)  # Execute the command to download the audio
        print(f"Downloaded: {video_url}")

        # Pause for 2 seconds before downloading the next file
        print("⏳ Waiting for 2 seconds to prevent rate limiting...")
        time.sleep(2)

    # Embed the downloaded cover image into each MP3 file
    for filename in os.listdir(output_folder):
        if filename.endswith(".mp3"):
            audio_path = os.path.join(output_folder, filename)
            thumbnail_path = audio_path.replace(".mp3", ".jpg")  # Expected thumbnail file

            # Check if the thumbnail exists and embed it into the MP3 file
            if os.path.exists(thumbnail_path):
                print(f"🎨 Embedding cover for {filename}...")

                temp_output = audio_path.replace(".mp3", "_with_cover.mp3")  # Temporary output file

                # ffmpeg command to embed cover image into the MP3 file
                ffmpeg_command = [
                    FFMPEG_PATH,
                    "-i", audio_path,  # Input audio file
                    "-i", thumbnail_path,  # Input thumbnail image
                    "-map", "0:a",  # Use only the audio stream from input 0
                    "-map", "1:v",  # Use only the image stream from input 1
                    "-c:a", "copy",  # Copy audio without re-encoding
                    "-c:v", "jpeg",  # Convert image to JPEG format
                    "-id3v2_version", "3",  # Use ID3v2.3 tag version for compatibility
                    temp_output
                ]

                subprocess.run(ffmpeg_command)  # Execute the command to embed the cover image
                os.replace(temp_output, audio_path)  # Replace the original file with the new one

    print("All songs downloaded with cover images!!")

# Get the playlist URL and output folder path
playlist_url = input("Enter YouTube Playlist URL: ")
output_folder = r"C:\Users\xxxx\Desktop\songs" #add your optput path

# Start downloading the playlist
download_audio_with_cover(playlist_url, output_folder)
