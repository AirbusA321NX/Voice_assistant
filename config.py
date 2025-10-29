# config.py
import os

# Voice Assistant Configuration

# Audio settings
DEFAULT_RECORDING_DURATION = 3  # seconds
LONG_COMMAND_DURATION = 10      # seconds for complex commands

# Whisper model settings
WHISPER_MODEL = "medium"        # Options: "tiny", "base", "small", "medium", "large"
WHISPER_DEVICE = "cuda"         # Options: "cpu", "cuda"

# Ollama settings
OLLAMA_MODEL = "mistral:7b-instruct-q4_K_M"

# Application mappings
APPLICATION_COMMANDS = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "word": "start winword",
    "excel": "start excel",
    "powerpoint": "start powerpnt",
    "chrome": "start chrome",
    "firefox": "start firefox",
    "edge": "start msedge",
    "vlc": "start vlc",
    "spotify": "start spotify",
    "vscode": "start code",
    "pycharm": "start pycharm64.exe"
}

# System commands
SYSTEM_COMMANDS = {
    "shutdown": "shutdown /s /t 0",
    "restart": "shutdown /r /t 0",
    "lock": "rundll32.exe user32.dll,LockWorkStation",
    "task manager": "taskmgr",
    "command prompt": "start cmd",
    "powershell": "start powershell",
    "file explorer": "explorer"
}

# Media control commands (requires nircmd)
MEDIA_COMMANDS = {
    "mute": "nircmd mute 0",
    "unmute": "nircmd mute 1",
    "increase volume": "nircmd changesysvolume 10000",
    "decrease volume": "nircmd changesysvolume -10000",
    "screenshot": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms,System.Drawing; [System.Windows.Forms.SendKeys]::SendWait('{%PRTSC}')\""
}

# Activation phrases
ACTIVATION_PHRASES = ["hello assistant", "hey assistant", "ok assistant"]
STOP_PHRASES = ["stop assistant", "quit assistant", "exit assistant"]

# Settings URLs
SETTINGS_URLS = {
    "sound": "start ms-settings:sound",
    "network": "start ms-settings:network",
    "display": "start ms-settings:display",
    "wifi": "start ms-settings:network",
    "bluetooth": "start ms-settings:devices",
    "privacy": "start ms-settings:privacy",
    "updates": "start ms-settings:windowsupdate"
}