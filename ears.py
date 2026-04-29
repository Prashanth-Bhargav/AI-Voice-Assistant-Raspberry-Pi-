# ears.py
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# --- Configuration ---
SAMPLE_RATE = 16000
DEVICE_ID = 2  # The OPPO Buds index
STT_MODEL = "small.en" # English-only model for higher accuracy

# Initialize STT (The Ears)
print(f"Loading Whisper {STT_MODEL} model...")
whisper_model = WhisperModel(STT_MODEL, device="cpu", compute_type="int8")

def listen_and_transcribe(duration=5):
    """Records audio from the OPPO Buds and transcribes it."""
    try:
        print("\n[Listening...]")
        audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, 
                       channels=1, dtype="float32", device=DEVICE_ID)
        sd.wait()
        
        # VAD Filter added here to cut out dead silence and stop hallucinations
        segments, _ = whisper_model.transcribe(
            audio.squeeze(), 
            beam_size=5,
            vad_filter=True,
            condition_on_previous_text=False
        )
        
        text = " ".join([s.text for s in segments]).strip() 
        return text
    except Exception as e:
        print(f"Recording Error: {e}")
        return ""