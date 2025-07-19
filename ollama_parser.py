# ollama_parser.py
import subprocess
import json

def parse_command(user_input):
    prompt = prompt = f"""
You are a strict Windows 10/11 system assistant.

Your only task is to convert a human instruction into a valid Windows Command Prompt (cmd.exe) command. Return a **single JSON object** exactly like this:

{{
  "command": "a_valid_windows_command"
}}

 Strict Rules:
- Output ONLY a real Windows command that works in CMD
- DO NOT explain anything
- DO NOT invent or guess fake commands like 'control soundsettings'
- If no valid command exists, return: {{ "command": "" }}
- Always prefer GUI commands via `start ms-settings:*` when appropriate
- For web tasks, return a full URL with `start https://...`
- Never use Linux/Unix tools like wget, unzip, bash, or apt
- Only use commands available in Windows CMD (cmd.exe)

✅ Examples:

Input: "Open Notepad"
→ {{ "command": "notepad" }}

Input: "Shutdown my PC"
→ {{ "command": "shutdown /s /t 0" }}

Input: "Lock screen"
→ {{ "command": "rundll32.exe user32.dll,LockWorkStation" }}

Input: "Search python file IO"
→ {{ "command": "start https://www.google.com/search?q=python+file+IO" }}

Input: "Open YouTube"
→ {{ "command": "start https://www.youtube.com" }}

Input: "Open sound settings"
→ {{ "command": "start ms-settings:sound" }}

Input: "Open network settings"
→ {{ "command": "start ms-settings:network" }}

Input: "Open web browser"
→ {{ "command": "start chrome" }}

User: "{user_input}"

Now respond ONLY with the JSON object:
"""

    result = subprocess.run(["ollama", "run", "mistral:7b-instruct-q4_K_M"], input=prompt.encode(), capture_output=True)
    output = result.stdout.decode()

    try:
        first = output.index("{")
        last = output.rindex("}")
        json_part = output[first:last+1]
        return json.loads(json_part)
    except:
        return {"command": ""}
