
from yt_utils import download_audio_stream, convert_to_mp3
import tempfile


def main(link: str, output_directory_prefix: str):
    print(f'downloading {link} to {output_directory_prefix}')
    temp_dir = tempfile.mkdtemp()
    temp_file = download_audio_stream(link, temp_dir, output_directory_prefix)
    convert_to_mp3(temp_file, output_directory_prefix)


if __name__ == "__main__":
    song_url = input("Please enter the url of the song you wish to download: ")
    output_dir = input("Please enter the path to download the audio to: ")
    main(song_url, output_dir)
