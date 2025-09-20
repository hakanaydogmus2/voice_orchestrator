from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    deepgram_api_key: str 
    openai_api_key: str 
    elevenlabs_api_key: str 
    elevenlabs_voice_id: str
    elevenlabs_model: str
    openai_model: str
    deepgram_model: str
    deepgram_language: str
    log_dir: str


settings = Settings()