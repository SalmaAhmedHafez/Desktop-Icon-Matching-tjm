import os
from pathlib import Path

# Application Target
TARGET_ICON_TEXT = "Notepad"
TARGET_PROCESS_NAME = "notepad.exe"

# Filesystem
PROJECT_DIR_NAME = "tjm-project"
SCREENSHOT_FILENAME = "current_desktop.png"
DEBUG_FILENAME = "debug_detection_result.png"

# Path to the reference icon inside the project folder
BASE_DIR = Path(__file__).parent.parent
REFERENCE_ICON_NAME = "reference_icon.png"

# OCR Settings
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
MATCH_THRESHOLD = 85

# API Settings
API_URL = "https://jsonplaceholder.typicode.com/posts"
POST_LIMIT = 10
API_TIMEOUT = 2 

# Vision
ICON_VERTICAL_OFFSET = 50 
