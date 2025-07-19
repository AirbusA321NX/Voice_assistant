# task_dispatcher.py
import subprocess

def dispatch_command(command):
    try:
        args = ["build/sys_control.exe"] + command.split()
        subprocess.run(args)
    except Exception as e:
        print("❌ Error running system command via C++:", e)
