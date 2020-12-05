import os
import subprocess
from pytube import Playlist, YouTube
from pytube.exceptions import RegexMatchError
from typing import Optional


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