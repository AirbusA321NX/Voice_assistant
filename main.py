import tkinter as tk
from tkinter import messagebox
import threading
import time
import urllib.parse

from voice_input import get_voice_command, get_long_voice_command
from ollama_parser import parse_command
from task_dispatcher import dispatch_command, launch_application
from info_handler import handle_information_request
import config

def show_popup():
    """Show a popup indicating the assistant is running"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Voice Assistant", "Assistant is now running!\nSay commands or 'Stop Assistant' to exit.")
    root.destroy()

def show_listening_popup():
    """Show a popup indicating the assistant is listening"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Voice Assistant", "Listening... Say your command.")
    root.destroy()

def show_error_popup(message):
    """Show an error popup with the given message"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Voice Assistant - Error", message)
    root.destroy()

def handle_web_search(query):
    """Handle web search requests"""
    search_url = f"start https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    try:
        dispatch_command(search_url)
        print(f"🔍 Searching for: {query}")
    except Exception as e:
        error_msg = f"❌ Failed to execute web search: {str(e)}"
        print(error_msg)
        show_error_popup(error_msg)

def handle_long_command():
    """Handle longer, more complex commands"""
    print("🎙️ Listening for complex command...")
    voice_text = get_long_voice_command(duration=config.LONG_COMMAND_DURATION)
    voice_text_str = str(voice_text) if voice_text is not None else ""
    
    if voice_text_str.strip() == "":
        print("⚠️ No command detected.")
        return
        
    print("🗣️ You said:", voice_text_str)
    
    # Use AI parser for complex commands
    parsed = parse_command(voice_text_str)
    command = parsed.get("command", "")

    if command:
        print("🚀 Running:", command)
        try:
            result = dispatch_command(command)
            print("✅ Command executed successfully:", result)
        except Exception as e:
            error_msg = f"❌ Failed to execute command: {str(e)}"
            print(error_msg)
            show_error_popup(error_msg)
    else:
        print("⚠️ Could not understand the instruction.")
        show_error_popup("Sorry, I couldn't understand that command.")

print("🎤 Say 'Hello Assistant' to start...")

# Wait for activation phrase
while True:
    voice_text = get_voice_command()
    # Ensure voice_text is treated as a string
    voice_text_str = str(voice_text) if voice_text is not None else ""
    
    # Check for any activation phrase
    activated = any(phrase in voice_text_str.lower() for phrase in config.ACTIVATION_PHRASES)
    
    if activated:
        print("👋 Assistant activated!")
        # Show popup in a separate thread to avoid blocking
        popup_thread = threading.Thread(target=show_popup)
        popup_thread.start()
        time.sleep(0.1)  # Give time for popup to appear
        break
    elif voice_text_str.strip() != "":
        print("🔇 Say 'Hello Assistant' to activate...")

# Main command loop
print("🎙️ Listening for commands...")
while True:
    voice_text = get_voice_command()
    # Ensure voice_text is treated as a string
    voice_text_str = str(voice_text) if voice_text is not None else ""
    if voice_text_str.strip() == "":
        continue
        
    # Check for stop phrases
    if any(phrase in voice_text_str.lower() for phrase in config.STOP_PHRASES):
        print("👋 Assistant stopped.")
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Voice Assistant", "Assistant stopped. Goodbye!")
        root.destroy()
        break
        
    if "long command" in voice_text_str.lower() or "complex command" in voice_text_str.lower():
        handle_long_command()
        continue

    print("🗣️ You said:", voice_text_str)
    
    # Check for information queries through AI
    ai_response = handle_information_request(voice_text_str)
    if ai_response:
        try:
            action = ai_response.get("action", "")
            if action == "web_search":
                query = ai_response.get("query", "")
                handle_web_search(query)
                continue
            elif action == "system_command":
                # Let the normal flow handle system commands
                pass
        except Exception as e:
            error_msg = f"❌ Failed to process AI response: {str(e)}"
            print(error_msg)
            show_error_popup(error_msg)

    # Use AI parser for complex commands
    parsed = parse_command(voice_text_str)
    command = parsed.get("command", "")

    if command:
        print("🚀 Running:", command)
        try:
            result = dispatch_command(command)
            print("✅ Command executed successfully:", result)
        except Exception as e:
            error_msg = f"❌ Failed to execute command: {str(e)}"
            print(error_msg)
            show_error_popup(error_msg)
    else:
        print("⚠️ Could not understand the instruction.")
        show_error_popup("Sorry, I couldn't understand that command.")