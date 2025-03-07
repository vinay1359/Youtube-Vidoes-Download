# YouTube Playlist Downloader

A collection of Python scripts to download YouTube playlists as either audio-only MP3 files with embedded cover art or as high-quality MP4 videos.

## 📋 Features

- **Audio-Only Mode**: Downloads songs from playlists with album artwork embedded
- **Video Mode**: Downloads full videos in the best available quality
- **Smart Rate Limiting**: Prevents YouTube from blocking your downloads
- **Automatic Format Selection**: Always gets the best quality available

## 🛠️ Prerequisites

This tool requires two external dependencies:

### 1. yt-dlp

yt-dlp is a powerful YouTube downloader, fork of youtube-dl with additional features and fixes.

#### Installation:
```bash
pip install yt-dlp
```

#### Why yt-dlp?
- Faster downloads than youtube-dl
- Active maintenance and updates
- Better handling of throttling
- More format options

#### How yt-dlp Works:
`yt-dlp` fetches video metadata from YouTube and allows users to download the best available video/audio streams. It supports downloading separate audio and video streams and merging them with FFmpeg when necessary. Additionally, it can bypass certain restrictions like throttling and regional limitations.

### 2. FFmpeg

FFmpeg is essential for processing audio/video files. It handles:
- Converting between formats
- Extracting audio from video
- Merging audio and video streams
- Embedding album artwork into MP3 files

#### Installation on Windows:

1. **Download FFmpeg:**
   - Visit [gyan.dev FFmpeg builds](https://www.gyan.dev/ffmpeg/builds/)
   - Download the "ffmpeg-git-full.7z" file (or ZIP version)

2. **Extract the Files:**
   - Use 7-Zip or WinRAR to extract the downloaded archive
   - Pro tip: Consider saving to a drive other than C: to preserve your installation if your OS needs reinstalling

3. **Add to System PATH:**
   - Copy the full path to the `bin` folder inside the extracted directory
   - Open "Edit the system environment variables" from Windows search
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and paste the path to the bin folder
   - Click "OK" on all dialogs

4. **Verify Installation:**
   - Open Command Prompt or PowerShell
   - Type `ffmpeg -version` and press Enter
   - You should see version information if installed correctly

#### Installation on macOS:
```bash
brew install ffmpeg
```

#### Installation on Linux:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### How FFmpeg Works:
FFmpeg is a multimedia framework that processes video and audio files. It enables:
- **Audio Extraction**: Extracts audio from video files.
- **Format Conversion**: Converts between MP4, MP3, and other formats.
- **Muxing/Demuxing**: Combines audio and video streams or separates them.
- **Thumbnail Embedding**: Inserts the video thumbnail into an MP3 file as album artwork.

## 🚀 Usage

### Audio-Only Downloader

This script downloads each video in the playlist as an MP3 file and embeds the video thumbnail as album artwork.

```bash
python download_playlist_audio_only.py
```

When prompted, enter the YouTube playlist URL.

### Video Downloader

This script downloads each video in the playlist at the best available quality.

```bash
python download_playlist_videos.py
```

When prompted, enter the YouTube playlist URL.

### Single Video Downloader

This script downloads a single video in the best available quality.

```bash
python download_video.py
```

When prompted, enter the YouTube video URL.

## ⚙️ Customization

You can modify these scripts to:

- Change output quality
- Adjust download speed limits
- Change the output directory (currently set to `C:\Users\bhara\Desktop\songs`)
- Modify waiting times between downloads

## 📝 Notes

- Boost your download speed significantly with this [pro tip](https://www.youtube.com/watch?v=dQw4w9WgXcQ).

- These scripts use rate limiting to prevent YouTube from blocking your IP address
- A sleep delay is added between downloads to reduce the risk of IP bans (testing has shown no bans so far)
- Downloads might take time depending on your internet speed and playlist size
- The audio-only script includes a 2-second delay between downloads
- The video script includes a 5-second delay between downloads

## ⚠️ Legal Notice

This tool is meant for downloading content that you have permission to download. Please respect copyright laws and YouTube's Terms of Service.

