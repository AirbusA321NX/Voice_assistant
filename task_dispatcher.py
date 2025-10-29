# task_dispatcher.py
import subprocess
import os
import config

def dispatch_command(command):
    if not command or not isinstance(command, str):
        raise ValueError("Invalid command: Command must be a non-empty string")
    
    try:
        # Check if it's a web URL command
        if command.startswith("start https://") or command.startswith("start http://"):
            # For web URLs, we can use os.system for simplicity
            os.system(command)
            return "Web command executed successfully"
        else:
            # For other commands, use the C++ helper
            args = ["build/sys_control.exe"] + command.split()
            result = subprocess.run(args, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Command failed with exit code {result.returncode}: {result.stderr}")
                
            if result.stdout:
                print(result.stdout)
                return result.stdout.strip()
            return "Command executed successfully"
                
    except FileNotFoundError:
        # Fallback if sys_control.exe is not found
        print("⚠️ C++ helper not found, trying direct execution...")
        os.system(command)
        return "Command executed with fallback method"
    except Exception as e:
        print("❌ Error running system command:", e)
        raise

def launch_application(app_name):
    """Launch an application by name with better error handling"""
    if app_name.lower() in config.APPLICATION_COMMANDS:
        try:
            dispatch_command(config.APPLICATION_COMMANDS[app_name.lower()])
            return f"Launching {app_name}..."
        except Exception as e:
            return f"Failed to launch {app_name}: {str(e)}"
    else:
        return f"Application {app_name} not recognized. Try another application."

def execute_system_command(command_name):
    """Execute a system command by name"""
    if command_name.lower() in config.SYSTEM_COMMANDS:
        try:
            dispatch_command(config.SYSTEM_COMMANDS[command_name.lower()])
            return f"Executing {command_name}..."
        except Exception as e:
            return f"Failed to execute {command_name}: {str(e)}"
    else:
        return f"System command {command_name} not recognized."

def control_media(action):
    """Control media playback"""
    if action.lower() in config.MEDIA_COMMANDS:
        try:
            dispatch_command(config.MEDIA_COMMANDS[action.lower()])
            return f"Media action '{action}' executed."
        except Exception as e:
            return f"Failed to execute media action '{action}': {str(e)}"
    else:
        return f"Media action '{action}' not recognized."

def open_settings(setting_name):
    """Open system settings"""
    if setting_name.lower() in config.SETTINGS_URLS:
        try:
            dispatch_command(config.SETTINGS_URLS[setting_name.lower()])
            return f"Opening {setting_name} settings..."
        except Exception as e:
            return f"Failed to open {setting_name} settings: {str(e)}"
    else:
        return f"Settings for {setting_name} not recognized."