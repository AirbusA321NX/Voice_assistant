import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave

# pylint: disable=no-member

# Load the Whisper model
model = whisper.load_model("medium").to("cuda")

def record_audio(filename, duration=3, fs=16000):
    print("🎤 Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Save as proper 16-bit WAV using wave module (not scipy)
    with wave.open(filename, 'wb') as wf:  # pylint: disable=attribute-defined-outside-init
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

def get_voice_command(duration=3) -> str:
    # For quicker responses to short commands, we can try a shorter recording first
    if duration > 2:
        # Try a quick 1-second recording first for short commands
        quick_result = _get_quick_command(1)
        if quick_result and quick_result.strip():
            return quick_result
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    record_audio(temp_path, duration=duration)

    # Optional: Verify file is readable by ffmpeg
    if not os.path.exists(temp_path) or os.path.getsize(temp_path) < 1000:
        print("Audio file was not properly saved.")
        return ""

    try:
        result = model.transcribe(temp_path)
        text_result = result["text"] if isinstance(result["text"], str) else str(result["text"])
        print("You said:", text_result)
        return text_result
    except Exception as e:
        print("Whisper error:", str(e))
        return ""
    finally:
        os.remove(temp_path)

def _get_quick_command(duration=1) -> str:
    """Helper function to quickly capture short commands"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    record_audio(temp_path, duration=duration)

    try:
        result = model.transcribe(temp_path)
        text_result = result["text"] if isinstance(result["text"], str) else str(result["text"])
        # If we got a very short transcription, it might be a quick command
        if len(text_result.strip()) < 20 and text_result.strip():
            return text_result
        return ""
    except Exception:
        return ""
    finally:
        os.remove(temp_path)

def get_long_voice_command(duration=10) -> str:
    """Get a longer voice command for complex instructions"""
    print("🎤 Listening for longer command...")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    record_audio(temp_path, duration=duration)

    try:
        result = model.transcribe(temp_path)
        text_result = result["text"] if isinstance(result["text"], str) else str(result["text"])
        print("You said:", text_result)
        return text_result
    except Exception as e:
        print("Whisper error:", str(e))
        return ""
    finally:
        os.remove(temp_path)