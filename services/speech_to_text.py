from openai import OpenAI
from dotenv import load_dotenv
import os

def speech_to_text(audio_file):
    """
    Transcribes speech from an audio file to text.
    
    Parameters:
    audio_file (str): Path to the input audio file
    """

    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    audio_data= open(audio_file, "rb")
    
    client = OpenAI(api_key = openai_api_key)
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_data
    )
    return transcription.text