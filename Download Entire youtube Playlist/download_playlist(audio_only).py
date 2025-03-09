import os
import subprocess
import shutil
import time
import glob
import re

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
    
    # Create or ensure the downloaded archive file exists
    archive_path = os.path.join(output_folder, "downloaded.txt")
    if not os.path.exists(archive_path):
        open(archive_path, 'a').close()
    
    # Get the list of video URLs and titles from the playlist
    print("🔍 Fetching playlist information...")
    command = [
        YT_DLP_PATH, 
        "--flat-playlist", 
        "--print", "%(url)s|%(title)s", 
        f"{playlist_url}"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    playlist_items = result.stdout.strip().split("\n")
    
    # Parse the results
    videos = []
    for item in playlist_items:
        if item and "|" in item:
            url, title = item.split("|", 1)
            videos.append({"url": url.strip(), "title": title.strip()})
    
    if not videos:
        print("No videos found in the playlist or invalid playlist URL.")
        return

    print(f"🔍 Found {len(videos)} videos in the playlist")
    
    # Read the archive file to check which videos are already downloaded
    already_downloaded = set()
    if os.path.exists(archive_path):
        with open(archive_path, 'r') as f:
            for line in f:
                if line.strip():
                    video_id = line.strip().split(' ')[1]
                    already_downloaded.add(video_id)
    
    # Track statistics
    new_downloads = 0
    skipped_downloads = 0
    failed_downloads = 0
    deleted_thumbnails = 0

    # Loop through each video in the playlist
    for index, video in enumerate(videos, start=1):
        video_url = video["url"]
        video_title = video["title"]
        
        # Extract video ID from URL
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_url)
        if not video_id_match:
            print(f"Could not extract video ID from URL: {video_url}")
            continue
            
        video_id = video_id_match.group(1)
        
        print(f"\n🔹 Processing {index}/{len(videos)}: {video_title}")
        
        # Check if video is already in the archive
        if f"youtube {video_id}" in already_downloaded:
            print(f"Already downloaded before again why you will downlaod (idiot): {video_title}")
            skipped_downloads += 1
            continue
        
        # Create a safe filename
        safe_title = "".join([c if c.isalnum() or c in ' -_' else '_' for c in video_title]).strip()
        output_template = os.path.join(output_folder, f"{safe_title}.%(ext)s")
        
        # Download the video as audio with thumbnail
        print(f"Downloading: {video_title}")
        
        command = [
            YT_DLP_PATH,
            "-f", "bestaudio",  # Select the best audio format available
            "--extract-audio",  # Extract audio only
            "--audio-format", "mp3",  # Convert to MP3 format
            "--audio-quality", "0",  # Highest audio quality
            "--output", output_template,  # Save with sanitized video title
            "--write-thumbnail",  # Download thumbnail as a cover image
            "--convert-thumbnails", "jpg",  # Convert thumbnails to jpg
            "--sleep-interval", "2",  # Wait 2 seconds between downloads
            "--limit-rate", "1M",  # Limit download speed to prevent blocking
            "--no-warnings",  # Suppress warnings
            "--download-archive", archive_path,  # Track downloaded songs
            "--no-post-overwrites",  # Skip existing files
            video_url
        ]
        
        try:
            download_process = subprocess.run(command, capture_output=True, text=True)
            
            # Check for the downloaded MP3 file
            mp3_path = os.path.join(output_folder, f"{safe_title}.mp3")
            if not os.path.exists(mp3_path):
                # Try to find the MP3 with a similar name (in case yt-dlp changed the filename)
                possible_mp3s = glob.glob(os.path.join(output_folder, f"{safe_title}*.mp3"))
                if possible_mp3s:
                    mp3_path = possible_mp3s[0]
            
            # Find all possible thumbnails for this video
            thumbnails_to_delete = []
            possible_thumbnails = []
            possible_thumbnails.extend(glob.glob(os.path.join(output_folder, f"{safe_title}*.jpg")))
            possible_thumbnails.extend(glob.glob(os.path.join(output_folder, f"{safe_title}*.webp")))
            
            # Convert any webp files to jpg
            thumbnail_path = None
            for thumb in possible_thumbnails:
                thumbnails_to_delete.append(thumb)  # Add to delete list
                
                if thumb.endswith('.webp'):
                    jpg_path = thumb.replace('.webp', '.jpg')
                    convert_cmd = [
                        FFMPEG_PATH,
                        "-i", thumb,
                        "-y",  # Overwrite output files without asking
                        jpg_path
                    ]
                    subprocess.run(convert_cmd, capture_output=True)
                    if os.path.exists(jpg_path):
                        thumbnails_to_delete.append(jpg_path)  # Also add the jpg to delete list
                        thumbnail_path = jpg_path
                else:
                    thumbnail_path = thumb
            
            # Embed the thumbnail into the MP3 if both files exist
            embedding_success = False
            if os.path.exists(mp3_path) and thumbnail_path and os.path.exists(thumbnail_path):
                print(f"Embedding cover art for {os.path.basename(mp3_path)}...")
                
                temp_output = mp3_path.replace(".mp3", "_with_cover.mp3")
                
                # ffmpeg command to embed cover image
                ffmpeg_command = [
                    FFMPEG_PATH,
                    "-i", mp3_path,  # Input audio file
                    "-i", thumbnail_path,  # Input thumbnail image
                    "-map", "0:a",  # Use only the audio stream from input 0
                    "-map", "1",  # Use the image from input 1
                    "-c:a", "copy",  # Copy audio without re-encoding
                    "-id3v2_version", "3",  # Use ID3v2.3 tag version for compatibility
                    "-metadata:s:v", "title=Album cover",
                    "-metadata:s:v", "comment=Cover (front)",
                    "-y",  # Overwrite output files without asking
                    temp_output
                ]
                
                try:
                    subprocess.run(ffmpeg_command, capture_output=True, check=True)
                    # Replace original file with the one containing the cover
                    os.replace(temp_output, mp3_path)
                    print(f"Successfully embedded cover for {os.path.basename(mp3_path)}")
                    embedding_success = True
                except subprocess.CalledProcessError as e:
                    print(f"First embedding method failed: {e}")
                    # Try alternative method for embedding cover
                    alt_ffmpeg_command = [
                        FFMPEG_PATH,
                        "-i", mp3_path,
                        "-i", thumbnail_path,
                        "-map", "0",
                        "-map", "1",
                        "-c", "copy",
                        "-disposition:v:0", "attached_pic",
                        "-y",
                        temp_output
                    ]
                    try:
                        subprocess.run(alt_ffmpeg_command, capture_output=True, check=True)
                        os.replace(temp_output, mp3_path)
                        print(f" Successfully embedded cover using alternative method")
                        embedding_success = True
                    except subprocess.CalledProcessError:
                        print(f"Both embedding methods failed for {os.path.basename(mp3_path)}")
                
                # Delete thumbnails immediately after successful embedding
                if embedding_success:
                    for thumb in thumbnails_to_delete:
                        if os.path.exists(thumb):
                            try:
                                os.remove(thumb)
                                deleted_thumbnails += 1
                                print(f"🗑️ Deleted: {os.path.basename(thumb)}")
                            except Exception as e:
                                print(f"Could not delete {os.path.basename(thumb)}: {str(e)}")
                    
                    new_downloads += 1
                    print(f"Successfully downloaded and processed: {video_title}")
                else:
                    failed_downloads += 1
                    print(f"Failed to embed thumbnail for: {video_title}")
            else:
                if os.path.exists(mp3_path):
                    print(f"Already downloaded before again why you will download (idiot): {video_title}")
                    new_downloads += 1  # Still count as a success since we got the audio
                else:
                    print(f"Failed to download: {video_title}")
                    failed_downloads += 1
        
        except Exception as e:
            failed_downloads += 1
            print(f" Error processing {video_url}: {str(e)}")
        
        # Pause before downloading the next file if not the last one
        if index < len(videos):
            print("⏳ Waiting for 2 seconds to prevent rate limiting...")
            time.sleep(2)
    
    # Show final summary
    print("\nDownload Summary: super bro u downlaoded all enjoy")
    print(f" New downloads: {new_downloads} songs")
    print(f" Skipped (already downloaded): {skipped_downloads} songs")
    print(f" Failed downloads: {failed_downloads} songs")
    print(f" Cleaned up {deleted_thumbnails} thumbnail files")
    print(f" Files saved to: {os.path.abspath(output_folder)}")
    
    # Final sweep for any leftover image files (optional safety measure)
    if input("\nWould you like to check for any remaining image files to delete? (y/n): ").lower() == 'y':
        leftover_images = glob.glob(os.path.join(output_folder, "*.jpg"))
        leftover_images.extend(glob.glob(os.path.join(output_folder, "*.webp")))
        leftover_images.extend(glob.glob(os.path.join(output_folder, "*.png")))
        
        if leftover_images:
            print(f"Found {len(leftover_images)} leftover image files.")
            if input("Delete these files? (y/n): ").lower() == 'y':
                deleted_count = 0
                for img in leftover_images:
                    try:
                        os.remove(img)
                        deleted_count += 1
                        print(f"🗑️ Deleted: {os.path.basename(img)}")
                    except Exception as e:
                        print(f"⚠️ Could not delete {os.path.basename(img)}: {str(e)}")
                print(f"🧹 Cleaned up {deleted_count} additional image files")
        else:
            print("No leftover image files found.")

if __name__ == "__main__":
    # Get the playlist URL and output folder path
    playlist_url = input("Enter YouTube Playlist URL: ")
    default_output = r"C:\Users\xxxx\Desktop\peace"
    
    output_folder = input(f"Enter output folder path (or press Enter for default: {default_output}): ")
    if not output_folder:
        output_folder = default_output
    
    # Start downloading the playlist
    download_audio_with_cover(playlist_url, output_folder)