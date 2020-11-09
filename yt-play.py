import os
import subprocess

from pytube import Playlist, YouTube
import requests
from bs4 import BeautifulSoup
import tempfile
from typing import List
import time
from typing import Optional

from pytube.exceptions import RegexMatchError


def main(playlist_url: str, output_directory_prefix: str):
    print(f'Downloading playlist {playlist_url} to {output_directory_prefix}')
    if not os.path.exists(output_directory_prefix):
        os.mkdir(output_directory_prefix)
    temp_dir = tempfile.mkdtemp()
    print(f'Using {temp_dir} as a temporary folder for webm files.')

    temp_files = download_playlist(playlist_url, temp_dir)
    for temp_file in temp_files:
        convert_to_mp3(temp_file, output_directory_prefix)
    print(f'Download complete: {output_directory_prefix}')


def convert_to_mp3(file_path: str, output_directory_prefix: str):
    """
    Uses the library ffmpeg to convert webm audio to mp3.
    :param file_path: The webm file path (this file is in the temporary work folder).
    :param output_directory_prefix: The output directory of the file.
    :return:
    """
    file_name = os.path.split(file_path)[1]
    file_title = os.path.splitext(file_name)[0]
    file_output = os.path.join(output_directory_prefix, file_title + '.mp3')
    subprocess.run([
        'ffmpeg',
        '-i',
        file_path,
        file_output])
    return None


def download_playlist(playlist_url: str, temp_dir: str) -> List:
    """
    Download all audio content from a YouTube's playlist.
    :param playlist_url: The URL of the playlist in string format.
    :param temp_dir: The temporary work folder (uses the system temporary folder).
    :return: The list of downloaded files within the temporary folder.
    """
    temp_files_list = []
    links = Playlist(playlist_url)
    for link in links:
        print(f'Processing {link}')
        temp_file_path = download_audio_stream(link, temp_dir)
        if temp_file_path:
            temp_files_list.append(temp_file_path)
        time.sleep(2)
    return temp_files_list


def download_audio_stream(link: str, temp_dir: str, try_count=0) -> Optional[str]:
    """
    Download the audio from a youtube video.
    :param link: The youtube video link as a string.
    :param temp_dir: The temporary output directory.
    :param try_count: The number of time the download was tried.
    :return: The full file path of the downloaded audio file.
    """
    try:
        yt = YouTube(link)
        best_audio_stream = yt.streams.filter(type='audio').order_by('abr').desc().first()
        file_path = best_audio_stream.download(output_path=temp_dir)
        return file_path
    except RegexMatchError:
        if try_count == 3:
            print(f'Error processing {link}')
            return None
        return download_audio_stream(link, temp_dir, try_count + 1)


def playlist_name(playlist_url) -> Optional[str]:
    """
    Extract the playlist's name using BeautifulSoup.
    :param playlist_url: The url of the playlist.
    :return: The playlist's name.
    """
    res = requests.get(playlist_url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    f = soup.find('title')
    return f.text.strip().replace(' - YouTube', '')


if __name__ == "__main__":
    pl_url = input("Please enter the url of the playlist you wish to download: ")
    output_dir = input("Please enter the path to download the audio to: ")
    main(pl_url, output_dir)
