# Voice Orchestrator 🎙️

Gerçek zamanlı ses -> metin -> LLM -> metin -> ses akışı orkestrasyonu. Mikrofon girdisini alır, Deepgram ile canlı olarak çözümler, OpenAI LLM ile yanıt üretir, ElevenLabs ile tekrar sese dönüştürür ve cevap verir

---
## Özellikler
- Canlı mikrofon dinleme (boşluk tuşu ile başlat/durdur)
- Akış bazlı STT (Deepgram)
- LLM entegrasyonu (OpenAI, model yapılandırılabilir)
- TTS çıktısı (ElevenLabs, model/voice ID yapılandırılabilir)
- `uv` ile hızlı ve deterministik bağımlılık yönetimi

---
## Mimari Genel Bakış
```
[Mikrofon] --(PCM chunks)--> [STT / Deepgram] --(text)--> [LLM / OpenAI]
	 --> (response text) --> [TTS / ElevenLabs] --(audio)--> [Çıkış / Oynatma]
																 \
																	-> [logs/conversation.jsonl]
```
Ana bileşenler:
- `src/audio.py` : Mikrofon akışı ve tuş dinleyici
- `src/stt_deepgram.py` : Deepgram gerçek zamanlı çözümleme
- `src/llm_openai.py` : OpenAI istemcisi
- `src/tts_elevenlabs.py` : ElevenLabs TTS çağrıları
- `src/orchestrator.py` : Akış orkestrasyonu
- `src/logger.py` : Günlükleme yardımcıları

---
## Gereksinimler
- Python 3.12+
- `uv` 
- Deepgram, OpenAI ve ElevenLabs API anahtarları
- FFmpeg kurulumu https://ffmpeg.org/ 
- Windows için https://github.com/BtbN/FFmpeg-Builds/releases/tag/latest ortam değişkenlerine eklenmeli
- linux için 
```bash
sudo apt update
sudo apt install ffmpeg
```

---
## Kurulum (Lokal, uv ile)
`uv` yoksa kurun:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# sonra PATH'e eklendiğinden emin olun (örn ~/.local/bin)
```
Bağımlılıkları senkronize edin:
```bash
uv sync
```

---
## Ortam Değişkenleri
`.env` dosyası oluşturup aşağıdakileri ekleyin
```
DEEPGRAM_API_KEY=
DEEPGRAM_MODEL=
DEEPGRAM_LANGUAGE=
OPENAI_API_KEY=
OPENAI_MODEL=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
ELEVENLABS_MODEL=
LOG_DIR=
```


## Çalıştırma (Lokal)

uv run main.py
```
Uygulama başladıktan sonra:
- Boşluk: Dinlemeyi başlat/durdur
- Enter: Uygulamayı sonlandır

