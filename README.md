# Vision-Based Desktop Automation

A high-accuracy Python automation agent that dynamically locates desktop icons using **Computer Vision** and **OCR**, interacts with the OS, and handles data with a robust "fallback" logic.

##  Core Logic & Flow

### 1. Data Fetching
The code first attempts to fetch 10 blog posts from an external API. 

### 2. Multi-Layered Vision Grounding 
To find the Notepad icon with high accuracy:
*   **Image Filtering:** It processes your screen through multiple filters (Adaptive & Luminance) to support both **Light** and **Dark** Windows themes.
*   **OCR + Fuzzy Logic:** It reads every word on your screen looking for "Notepad." It uses fuzzy matching to handle blurry text or minor OCR misreads.
*   **Visual Verification:** Once the text is found, it crops the area above the text and compares it to your `reference_icon.png` using Template Matching to verify it's the correct app.

### 3. Safe Automation 
*   **Save-on-Close:** Instead of using shortcuts, it triggers the "Save changes" dialog by trying to close the app (`Alt + F4`).
*   **The Safety Lock:** It uses `Alt + Y` to confirm overwriting existing files. This shortcut is smart—it replaces the file if it exists but does nothing if the file is new, preventing the bot from accidentally clicking other desktop items.

---

##  Prerequisites

*   **Python 3.10 or 3.11**: Required for library compatibility.
*   **Tesseract OCR**: 
    1.  [Download and install Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki).
    2.  Check your install path (Default: `C:\Program Files\Tesseract-OCR\tesseract.exe`).

---

## Installation


```bash
git clone https://github.com/SalmaAhmedHafez/tjm
cd tjm
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration (`src/config.py`)
You can change the bot's behavior in the `src/config.py` file without touching the logic:

| Variable | Description |
|---|---|
| `TARGET_ICON_TEXT` | Change this to "Chrome" or "Excel" to target other apps. |
| `TESSERACT_CMD` | Update this to point to your Tesseract installation. |
| `REFERENCE_ICON_NAME` | The name of your icon photo (Default: `reference_icon.png`). |
| `MATCH_THRESHOLD` | How strictly the bot checks the text/image (85% default). |


Simply run the main orchestrator:
```bash
python main.py
```

---

```text
├── main.py            # Entry point; manages the loop
├── reference_icon.png # Your target icon image
└── src/
    ├── config.py      # All settings and paths
    ├── vision.py      # OCR and Image processing
    ├── automation.py  # Keyboard and Mouse actions
    ├── data_loader.py # API fetching and offline backup
    └── utils.py       # DPI fixes and screenshots
```

Here are demo videos:
https://drive.google.com/drive/folders/1-7RU1gmNba4OeQc542eedBYh_QWFEGXF?usp=sharing
