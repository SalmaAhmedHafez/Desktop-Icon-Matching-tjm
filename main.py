import pyautogui
import time
from src import config, utils, data_loader, vision, automation

def main():
    utils.configure_dpi_awareness()
    pyautogui.FAILSAFE = True
    project_dir = utils.setup_project_directory()
    
    posts = data_loader.fetch_posts_data()
    
    for post in posts:
        launch_success = False
        for attempt in range(3):
            automation.prepare_desktop_view()
            screenshot_path = utils.take_desktop_screenshot(project_dir)
            if not screenshot_path: continue
            
            location = vision.find_icon_coordinates(screenshot_path, project_dir)
            if location:
                vision.save_debug_image(screenshot_path, location, project_dir)
                pyautogui.doubleClick(location[0], location[1])
                time.sleep(2.5)
                if utils.is_app_running():
                    launch_success = True
                    break
        
        if launch_success:
            automation.write_save_and_close(post, project_dir)
            time.sleep(1)

if __name__ == "__main__":
    main()
