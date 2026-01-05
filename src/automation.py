import pyautogui
import time
from src import config

def prepare_desktop_view():
    pyautogui.hotkey('win', 'd')
    time.sleep(2.0)

def write_save_and_close(post, project_dir):
    content = f"Title: {post['title']}\n\n{post['body']}"
    pyautogui.write(content, interval=0.01)
    time.sleep(0.5)
    
    pyautogui.hotkey('alt', 'f4')
    time.sleep(2.0) 
    
    pyautogui.press('enter') 
    time.sleep(2.5)
    
    full_save_path = str(project_dir / f"post_{post['id']}.txt")
    pyautogui.write(full_save_path, interval=0.01)
    time.sleep(0.5)
    
    pyautogui.press('enter')
    time.sleep(1.5)
    
    pyautogui.hotkey('alt', 'y')
    time.sleep(1.0)
