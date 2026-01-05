import os
import ctypes
import subprocess
from pathlib import Path
from PIL import ImageGrab
from src import config

def configure_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

def setup_project_directory():
    desktop = Path(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
    project_path = desktop / config.PROJECT_DIR_NAME
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path

def take_desktop_screenshot(save_dir):
    try:
        screenshot = ImageGrab.grab(all_screens=False)
        save_path = save_dir / config.SCREENSHOT_FILENAME
        screenshot.save(save_path)
        return str(save_path)
    except:
        return None

def is_app_running():
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        return config.TARGET_PROCESS_NAME.lower() in output.lower()
    except:
        return False
