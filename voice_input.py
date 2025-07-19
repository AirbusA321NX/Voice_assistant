import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave
import subprocess

# Load the Whisper model
model = whisper.load_model("medium").to("cuda")

def record_audio(filename, duration=5, fs=16000):
    print("🎤 Recording... Speak now")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Save as proper 16-bit WAV using wave module (not scipy)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

def get_voice_command():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    record_audio(temp_path)

    # Optional: Verify file is readable by ffmpeg
    if not os.path.exists(temp_path) or os.path.getsize(temp_path) < 1000:
        print("Audio file was not properly saved.")
        return ""

    try:
        result = model.transcribe(temp_path)
        print("You said:", result["text"])
        return result["text"]
    except Exception as e:
        print("Whisper error:", str(e))
        return ""
    finally:
        os.remove(temp_path)
