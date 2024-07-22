import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from dotenv import load_dotenv

_ = load_dotenv(dotenv_path=".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DIR_NOTES_PATH = os.getenv("DIR_NOTES_PATH")
DIR_AUDIO_PATH = os.getenv("DIR_AUDIO_PATH")
