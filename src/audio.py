import asyncio
import queue
import sounddevice as sd
from pynput import keyboard

class MicrophoneStream:
    def __init__(self, sample_rate=16000, blocksize=16000):
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self.audio_queue = queue.Queue()
        self.streaming = False
        self.listener_active = True

    def start_keyboard_listener(self):

        def on_press(key):
            if key == keyboard.Key.space:
                self.streaming = not self.streaming
                if self.streaming:
                    print("▶️ Listening started...")
                else:
                    print("⏹️ Listening stopped.")
            elif key == keyboard.Key.enter:
                self.listener_active = False
                return False  
            
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"⚠️ Audio status: {status}")
        if self.streaming:
            self.audio_queue.put(indata.copy().tobytes())

    def start_stream(self):
        with sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.blocksize,
            channels=1,
            dtype='int16',
            callback=self.audio_callback
        ):
            while self.listener_active:
                sd.sleep(100)