<<<<<<< HEAD
# ollama_parser.py
import subprocess
import json

def parse_command(user_input):
    prompt_template = """
You are a strict Windows 10/11 system assistant.

Your only task is to convert a human instruction into a valid Windows Command Prompt (cmd.exe) command. Return a **single JSON object** exactly like this:

{
  "command": "a_valid_windows_command"
}

 Strict Rules:
- Output ONLY a real Windows command that works in CMD
- DO NOT explain anything
- DO NOT invent or guess fake commands like 'control soundsettings'
- If no valid command exists, return: { "command": "" }
- Always prefer GUI commands via `start ms-settings:*` when appropriate
- For web search queries, create appropriate Google search URLs
- For WhatsApp messaging, use the WhatsApp Web URL scheme
- For application launching, use the most appropriate command (e.g., "start chrome" for Chrome browser)
- Never use Linux/Unix tools like wget, unzip, bash, or apt
- Only use commands available in Windows CMD (cmd.exe)

Examples:

Input: "Open Notepad"
→ { "command": "notepad" }

Input: "Shutdown my PC"
→ { "command": "shutdown /s /t 0" }

Input: "Restart my computer"
→ { "command": "shutdown /r /t 0" }

Input: "Lock screen"
→ { "command": "rundll32.exe user32.dll,LockWorkStation" }

Input: "Mute system volume"
→ { "command": "nircmd mute 0" }

Input: "Increase volume"
→ { "command": "nircmd changesysvolume 10000" }

Input: "Decrease volume"
→ { "command": "nircmd changesysvolume -10000" }

Input: "Take screenshot"
→ { "command": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms,System.Drawing; [System.Windows.Forms.SendKeys]::SendWait('{%PRTSC}')\"" }

Input: "Open calculator"
→ { "command": "calc" }

Input: "Open file explorer"
→ { "command": "explorer" }

Input: "Open command prompt"
→ { "command": "start cmd" }

Input: "Open PowerShell"
→ { "command": "start powershell" }

Input: "Open task manager"
→ { "command": "taskmgr" }

Input: "What is artificial intelligence?"
→ { "command": "start https://www.google.com/search?q=artificial+intelligence" }

Input: "Who is the president of USA?"
→ { "command": "start https://www.google.com/search?q=president+of+USA" }

Input: "How to cook pasta?"
→ { "command": "start https://www.google.com/search?q=how+to+cook+pasta" }

Input: "Search python file IO"
→ { "command": "start https://www.google.com/search?q=python+file+IO" }

Input: "Open YouTube"
→ { "command": "start https://www.youtube.com" }

Input: "Play music on YouTube"
→ { "command": "start https://www.youtube.com/results?search_query=music" }

Input: "Open Gmail"
→ { "command": "start https://mail.google.com" }

Input: "Check my email"
→ { "command": "start https://mail.google.com" }

Input: "Open sound settings"
→ { "command": "start ms-settings:sound" }

Input: "Open network settings"
→ { "command": "start ms-settings:network" }

Input: "Open display settings"
→ { "command": "start ms-settings:display" }

Input: "Open web browser"
→ { "command": "start chrome" }

Input: "Send WhatsApp message to 1234567890 saying Hello"
→ { "command": "start https://web.whatsapp.com/send?phone=1234567890&text=Hello" }

Input: "Play music"
→ { "command": "start https://www.youtube.com/watch?v=450p7gcG5mg" }

Input: "Pause music"
→ { "command": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(' ')\"" }

Input: "Next track"
→ { "command": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{RIGHT}')\"" }

Input: "Previous track"
→ { "command": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{LEFT}')\"" }

Input: "Launch Chrome"
→ { "command": "start chrome" }

Input: "Start Excel"
→ { "command": "start excel" }

Input: "Open VS Code"
→ { "command": "start code" }

User: "{}"

Now respond ONLY with the JSON object:
"""
    prompt = prompt_template.format(user_input)

    result = subprocess.run(["ollama", "run", "mistral:7b-instruct-q4_K_M"], input=prompt.encode(), capture_output=True, check=False)
    output = result.stdout.decode()

    try:
        first = output.index("{")
        last = output.rindex("}")
        json_part = output[first:last+1]
        return json.loads(json_part)
    except (ValueError, IndexError):
        return {"command": ""}
=======
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
>>>>>>> 97ee0853eb57439965771430efc01c881605ad1f
