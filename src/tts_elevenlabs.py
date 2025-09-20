import queue
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from config import settings


class ElevenLabsTTS:
    def __init__(self):
        self.elevenlabs = ElevenLabs(api_key=settings.elevenlabs_api_key)
        self.tts_queue = queue.Queue()
    
    def text_to_speech_queue(self, text):
        self.tts_queue.put(text)
    
    def process_tts(self, text):
        audio = self.elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=settings.elevenlabs_voice_id,
            model_id=settings.elevenlabs_model,
            output_format="mp3_44100_128",
        )
        play(audio)