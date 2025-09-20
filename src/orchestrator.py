import threading
import queue
import sounddevice as sd
from .stt_deepgram import DeepgramSTT
from .audio import MicrophoneStream
from .llm_openai import OpenAILLM
from .tts_elevenlabs import ElevenLabsTTS
from .logger import JSONLogger

class Orchestrator:
    def __init__(self):
        
        self.dg_stt = DeepgramSTT()
        self.llm = OpenAILLM()
        self.tts = ElevenLabsTTS()
        self.mic_stream = MicrophoneStream(sample_rate=16000, blocksize=2048)
        self.logger = JSONLogger()

        self.current_user_text = None
        self.current_assistant_text = ""
        
        self.threads = []

    def stream_audio_to_deepgram(self):
        while self.mic_stream.listener_active:
            try:
                audio_chunk = self.mic_stream.audio_queue.get(timeout=0.1)
                self.dg_stt.send_audio(audio_chunk)
            except queue.Empty:
                continue

    def transcript_to_llm(self):
        while self.mic_stream.listener_active:
            try:
                transcript = self.dg_stt.transcript_queue.get(timeout=0.1)
                print(f"User said: {transcript}")
                self.current_user_text = transcript
                self.llm.generate_stream_response(transcript)
            except queue.Empty:
                pass

    def llm_to_speech(self):
        while True:
            try:
                response = self.llm.response_queue.get(timeout=0.1)
                print(f"LLM response: {response}")
                self.current_assistant_text += " " + response
                self.tts.process_tts(response)

                if response.endswith((".", "?", "!")):
                    self.logger.log_turn(
                        self.current_user_text,
                        self.current_assistant_text.strip()
                    )
                    self.current_assistant_text = ""
            except queue.Empty:
                pass

    def start(self):
        # Deepgram bağlantısını başlat
        if not self.dg_stt.start_connection():
            return

        # Klavye listener başlat
        self.mic_stream.start_keyboard_listener()

        # Thread'leri başlat
        self.threads = [
            threading.Thread(target=self.mic_stream.start_stream, daemon=True),
            threading.Thread(target=self.stream_audio_to_deepgram, daemon=True),
            threading.Thread(target=self.transcript_to_llm, daemon=True),
            threading.Thread(target=self.llm_to_speech, daemon=True),
        ]

        for t in self.threads:
            t.start()

        # Ana döngü
        while self.mic_stream.listener_active:
            sd.sleep(100)

        # Bağlantıyı kapat
        self.dg_stt.stop_connection()


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.start()
