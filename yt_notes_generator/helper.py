import streamlit as st
import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import google.generativeai as genai

from utils import GOOGLE_API_KEY, DIR_NOTES_PATH, DIR_AUDIO_PATH
from utils import TUTORIAL_ONLY, CLASS_LECTURE
from utils import save_as_md, extract_filename, download_youtube_audio
from custom_logger import logger

genai.configure(api_key=GOOGLE_API_KEY)


def generate_notes_audio(
    youtube_url: str, model_name: str, system_prompt: str, user_prompt: str
):
    audio_file_path = download_youtube_audio(dir_path=DIR_AUDIO_PATH, url=youtube_url)
    base_name, file_name = extract_filename(audio_file_path)
    logger.info(f"Uploading file...{base_name}")
    your_file = genai.upload_file(path=audio_file_path)

    logger.info("Generating notes...")
    logger.info(f"Model used: {model_name}")
    model = genai.GenerativeModel(
        model_name=model_name, system_instruction=system_prompt
    )
    responses = model.generate_content(
        [user_prompt, your_file],
        stream=True,
    )

    logger.info(f"Deleting file from system: {base_name}")
    os.remove(audio_file_path)

    return responses

