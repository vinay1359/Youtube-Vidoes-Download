import yt_dlp  # Import the yt-dlp library for downloading videos

def download_video(url):
    # Options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # Download best video and audio up to 1080p
        'merge_output_format': 'mp4',  # Merge audio and video into mp4 format
    }
    
    try:
        # Create a YoutubeDL object with the specified options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video from the provided URL
            ydl.download([url])
        
        print("Download completed!")  # Confirmation message after successful download
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error occurred: {e}")

# Sample video link to download
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Replace with your desired video URL
# Call the download_video function with the sample video URL
download_video(video_url)
