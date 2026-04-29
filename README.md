# 🤖 AI Voice Assistant (Raspberry Pi)

A modular, fully local voice assistant built on a Raspberry Pi that listens, thinks using cloud GPU inference, and speaks — all in a clean pipeline architecture.

---

## 🏗️ Architecture

```
[ You speak ]
     ↓
 ears.py  →  faster-whisper INT8 (local STT on Pi CPU)
     ↓
 advanced_brain.py  →  LangChain Agent + Cloudflare Workers AI (Qwen3-30B FP8)
     ↓
 mouth.py  →  Piper TTS via ONNX (local voice synthesis on Pi)
     ↓
[ Assistant speaks ]
```

---

## 🧩 Modules

| File | Role | Key Tech |
|---|---|---|
| `ears.py` | Speech-to-Text | faster-whisper `small.en`, INT8, VAD filter |
| `advanced_brain.py` | LLM Agent | LangChain, Cloudflare Workers AI, Qwen3-30B FP8 |
| `mouth.py` | Text-to-Speech | Piper TTS, `en_US-lessac-medium.onnx`, aplay |
| `main.py` | Orchestration loop | Sequential listen → think → speak pipeline |
| `load_dotenv.py` | Credential loader | python-dotenv, env validation |

---

## ✨ Features

- **Fully local STT & TTS** — runs on Raspberry Pi CPU with no cloud dependency for voice I/O
- **Cloud GPU inference** — Cloudflare Workers AI provides fast Qwen3-30B FP8 responses without managing a GPU
- **LangChain Agent with 3 custom tools:**
  - `web_search` — real-time DuckDuckGo search for news/weather/current events
  - `analyze_file` — reads files from the `jarvis_files/` folder on demand
  - `list_files` — lists all available files in the folder
- **VAD (Voice Activity Detection)** filter in Whisper to suppress silence hallucinations
- **Modular design** — each module can be swapped independently (e.g., replace Cloudflare with Ollama)

---

## 🛠️ Tech Stack

- **STT:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — CTranslate2 INT8 quantized Whisper
- **LLM:** [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) — `@cf/qwen/qwen3-30b-a3b-fp8`
- **Agent Framework:** [LangChain](https://www.langchain.com/)
- **TTS:** [Piper](https://github.com/rhasspy/piper) — `en_US-lessac-medium` ONNX model
- **Audio I/O:** `sounddevice`, `numpy`, `aplay`
- **Hardware:** Raspberry Pi (tested with OPPO Buds as mic input via USB)

---

## 🚀 Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/edge-ai-voice-assistant.git
cd edge-ai-voice-assistant
```

### 2. Install dependencies
```bash
pip install faster-whisper sounddevice numpy langchain langchain-openai langchain-community duckduckgo-search python-dotenv
```

> **Piper TTS** must be installed separately. Follow the [Piper installation guide](https://github.com/rhasspy/piper#installation).

### 3. Download the voice model
Download `en_US-lessac-medium.onnx` from the [Piper voices releases](https://github.com/rhasspy/piper/releases) and place it at:
```
/home/pi/Desktop/voicebot/voices/en_US-lessac-medium.onnx
```
Or update the `VOICE_MODEL` path in `mouth.py` to match your setup.

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your Cloudflare credentials:
```
ACCOUNT_ID=your_cloudflare_account_id
API_TOKEN=your_cloudflare_api_token
```

### 5. Set your audio device
Run `python -c "import sounddevice; print(sounddevice.query_devices())"` to list audio devices, then update `DEVICE_ID` in `ears.py` to match your microphone index.

### 6. Run the assistant
```bash
python main.py
```

---

## 📁 Project Structure

```
edge-ai-voice-assistant/
├── main.py              # Orchestration loop
├── ears.py              # STT module (faster-whisper)
├── advanced_brain.py    # LLM agent (LangChain + Cloudflare)
├── mouth.py             # TTS module (Piper)
├── load_dotenv.py       # Credential loader
├── .env.example         # Template for environment variables
├── .gitignore
└── assistant_files/     # Drop files here for the assistant to read (not tracked in git)
```

---

## 🔐 Security Notes

- **Never commit your `.env` file** — it contains your Cloudflare API token
- `.gitignore` excludes `.env`, `jarvis_files/`, and the ONNX voice model (large binary)
- Use `.env.example` to share required variable names safely

---

## 📌 Notes & Known Configurations

- Default recording duration is **5 seconds** per utterance (configurable in `main.py`)
- The assistant gives an immediate **"Okay."** acknowledgment before processing, to reduce perceived latency
- Whisper runs in `int8` mode on CPU for memory efficiency on the Pi
- `condition_on_previous_text=False` prevents Whisper from confabulating across turns

---

## 🗺️ Roadmap

- [ ] Wake word detection (openwakeword integration)
- [ ] Streaming TTS for faster first-word response
- [ ] Home automation tool (GPIO / MQTT)
- [ ] Swap Cloudflare for local Ollama when offline

---

## 👤 Author

**Prashanth Bhargav Nutalapathi**  
AI/ML Engineer | [LinkedIn](https://www.linkedin.com/in/prashanth-bhargav/) | [GitHub](https://github.com/Prashanth-Bhargav)
