import queue
import httpx
import logging
from deepgram.utils import verboselogs
import threading

from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions
)

from config import settings

class DeepgramSTT:
    def __init__(self):
        self.client_options = DeepgramClientOptions(
            options={"keepalive": "true"}
        )
        self.client = DeepgramClient(settings.deepgram_api_key, self.client_options)
        self.connection = self.client.listen.websocket.v("1")
        self.transcript_queue = queue.Queue()


    def on_message(self, conn, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if len(sentence.strip()) == 0:
            return
        print(f"🗣️ {sentence}")
        self.transcript_queue.put(sentence)
    
    
    def start_connection(self, model=settings.deepgram_model, language=settings.deepgram_language):
        self.connection.on(LiveTranscriptionEvents.Transcript, self.on_message)
        options = LiveOptions(
            model=model,
            language=language,
            encoding="linear16",
            sample_rate=16000,
            endpointing=0
        )

        if self.connection.start(options) is False:
            print("Failed to start connection")
            return
        return True
        

    def send_audio(self, audio_data):
        if audio_data and len(audio_data) > 0:
            self.connection.send(audio_data)

    
    def stop_connection(self):
        self.connection.finish()
        print("Connection closed.")
        
        