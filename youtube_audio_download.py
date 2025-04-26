import yt_dlp  # Import the yt-dlp library for downloading audio

def download_audio(url):
    # Options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',           # Select the best available audio quality
        'outtmpl': '%(title)s.%(ext)s',        # Name the file with the video title
        'postprocessors': [{                   # Post-processing to convert to mp3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',         # You can change quality (e.g., 320 for high quality)
        }],
    }
    
    try:
        # Create a YoutubeDL object with the specified options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the audio from the provided URL
            ydl.download([url])
        
        print("Audio download completed!")  # Confirmation message after successful download
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error occurred: {e}")

# Input URL from user
video_url = input("Enter Your URL: ")
# Call the download_audio function
download_audio(video_url)
