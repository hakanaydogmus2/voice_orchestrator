# Voice Orchestrator 🎙️

mikrofonunuzdan gelen sesi gerçek zamanlı olarak işleyip yanıt veren bir akış sistemi sunar. Ses akışı önce metne dönüştürülür (STT), ardından LLM ile yanıt üretilir ve tekrar sese çevrilir (TTS). Sonuç olarak, canlı ve doğal bir konuşma deneyimi sağlar.

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
- `src/stt_deepgram.py` : Deepgram ile STT
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
- Windows: [BtbN FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases/tag/latest) → PATH’e ekleyin
- Linux 
```bash
sudo apt update
sudo apt install ffmpeg
```

---
## Kurulum (Lokal, uv ile)
`uv` yüklü değilse kurun:

Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
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
```
uv run main.py
```
Uygulama başladıktan sonra:
- Boşluk: Dinlemeyi başlat/durdur
- Enter: Uygulamayı sonlandır

