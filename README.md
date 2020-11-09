# yt-play

Download youtube playlist to mp3 files. Requires ffmpeg installed (apt install ffmpeg).

## Requirements
- pytube
- requests
- beautifulsoup4

Easy install with pipenv.

## How
1. It will download only the highest bitrate audio file (webm format) from the youtube streams as a temporary file (the system temporary folder).
2. From the temporary folder, ffmpeg will convert the webm file to an mp3 file and place it into the specified output folder.

Sometimes, pytube fails to fetch config data, it will retry 3 times and log print a message into the console when it was unable to download the audio.

