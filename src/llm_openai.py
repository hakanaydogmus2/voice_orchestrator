import queue
from openai import OpenAI
from config import settings


class OpenAILLM:
    def __init__(self, model=settings.openai_model):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = model
        self.chat_history = []
        self.response_queue = queue.Queue()


    def generate_stream_response(self, question):

        self.chat_history.append({"role": "user", "content": question})

        # API çağrısı
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Lütfen kısa ve net yanıt ver. Türkçe cevapla."},
                *self.chat_history  
            ],
            stream=True,
        )

        full_response = ""
        buffer = ""

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                buffer += content

                if content in [".", "?", "!", "\n"]:
                    self.response_queue.put(buffer.strip())
                    buffer = ""

        if buffer.strip():
            self.response_queue.put(buffer.strip())


        self.chat_history.append({"role": "assistant", "content": full_response})