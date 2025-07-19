# main.py
from voice_input import get_voice_command
from ollama_parser import parse_command
from task_dispatcher import dispatch_command

while True:
    voice_text = get_voice_command()
    if voice_text.strip() == "":
        continue

    print("🗣️ You said:", voice_text)
    parsed = parse_command(voice_text)
    command = parsed.get("command", "")

    if command:
        print("🚀 Running:", command)
        dispatch_command(command)
    else:
        print("⚠️ Could not understand the instruction.")
