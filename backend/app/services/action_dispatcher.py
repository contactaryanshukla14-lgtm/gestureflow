import subprocess
import time

COOLDOWN_SECONDS = 3.0
_last_execution_times = {}

def dispatch_action(action: str):
    if not action or action == 'none' or not action.startswith('open_'):
        return

    now = time.time()
    last_time = _last_execution_times.get(action, 0)
    
    # Cooldown check
    if now - last_time < COOLDOWN_SECONDS:
        return

    _last_execution_times[action] = now

    try:
        if action == 'open_chrome':
            subprocess.Popen('start chrome', shell=True)
        elif action == 'open_vscode':
            subprocess.Popen('code', shell=True)
        elif action == 'open_whatsapp':
            subprocess.Popen('start whatsapp:', shell=True)
        elif action == 'open_folder':
            subprocess.Popen('explorer', shell=True)
        elif action == 'open_camera':
            subprocess.Popen('start microsoft.windows.camera:', shell=True)
        elif action == 'open_calculator':
            subprocess.Popen('calc', shell=True)
        elif action == 'open_notepad':
            subprocess.Popen('notepad', shell=True)
        elif action == 'open_paint':
            subprocess.Popen('mspaint', shell=True)
        elif action == 'open_folder':
            subprocess.Popen('explorer', shell=True)
        elif action == 'open_vscode':
            subprocess.Popen('code', shell=True)
        else:
            print(f"Unknown action: {action}")
    except Exception as e:
        print(f"Error executing {action}: {e}")
