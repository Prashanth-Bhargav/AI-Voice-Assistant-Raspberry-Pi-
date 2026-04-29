import subprocess
import tempfile
import os

VOICE_MODEL = "/home/pi/Desktop/voicebot/voices/en_US-lessac-medium.onnx"

def speak(text):
    print(f"Jarvis: {text}")
    # Write text to a temp file, feed to piper, play output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(text)
        tmp_path = f.name

    subprocess.run(
        f'piper --model {VOICE_MODEL} --output_raw < {tmp_path} 2>/dev/null | aplay -r 22050 -f S16_LE -t raw - 2>/dev/null',
        shell=True
    )
    os.unlink(tmp_path)  # cleanup temp file

def cleanup():
    pass


