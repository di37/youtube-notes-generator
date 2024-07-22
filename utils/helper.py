import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import re
from custom_logger import logger

from datetime import datetime
from yt_dlp import YoutubeDL


def save_as_md(file_path: str, content: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    logger.info(f"Saving content to {file_path}")
    with open(file_path, "w") as f:
        f.write(content)


def sanitize_filename(filename):
    # Remove file extension
    filename = os.path.splitext(filename)[0]

    # Replace any character that's not lowercase alphanumeric or dash with a dash
    sanitized = re.sub(r"[^a-z0-9-]", "-", filename.lower())

    # Remove leading and trailing dashes
    sanitized = sanitized.strip("-")

    # Replace multiple consecutive dashes with a single dash
    sanitized = re.sub(r"-+", "-", sanitized)

    return sanitized


def extract_filename(filepath):
    # Get the base name (file name with extension)
    base_name = os.path.basename(filepath)

    # Split the base name and extension
    file_name = os.path.splitext(base_name)[0]

    return base_name, file_name


def return_youtube_id(url: str):
    """
    Returns YouTube ID of the video.

    Args:
        url: youtube video link
    Returns:
        str: youtube id
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def get_youtube_title(url: str):
    """
    Get the title of a YouTube video.

    Args:
        url: youtube video link
    Returns:
        str: video title
    """
    ydl_opts = {"quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("title", None)


def download_youtube_audio(dir_path: str, url: str):
    try:
        youtube_id = return_youtube_id(url)
        if not youtube_id:
            raise ValueError("Invalid YouTube URL")

        video_title = get_youtube_title(url)
        if not video_title:
            raise ValueError("Could not retrieve video title")

        sanitized_title = sanitize_filename(video_title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{sanitized_title}_{timestamp}"
        output_file_path = os.path.join(dir_path, f"{output_filename}.mp3")

        ytdl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(dir_path, output_filename),
            "quiet": True,
        }

        with YoutubeDL(ytdl_opts) as ydl:
            ydl.cache.remove()
            ydl.download([url])

        logger.info(f"Successfully downloaded: {output_file_path}")
        return output_file_path

    except Exception as ex:
        logger.error(f"Error downloading audio: {str(ex)}")
        return None


if __name__ == "__main__":
    # Example usage
    # original_filename = "My Audio File (1).mp3"
    # sanitized_filename = sanitize_filename(original_filename)
    # print(sanitized_filename)  # Output: my-audio-file-1
    print(download_youtube_audio("data/audio", "https://youtu.be/VCwk0Xk1oR0"))
