import cv2
import pytesseract
from fuzzywuzzy import fuzz
from src import config

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

def _apply_filters(img):
    upscaled = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
    f1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 4)
    hls = cv2.cvtColor(upscaled, cv2.COLOR_BGR2HLS)
    _, binary = cv2.threshold(hls[:, :, 1], 200, 255, cv2.THRESH_BINARY)
    f2 = cv2.bitwise_not(binary)
    return [f1, f2]

def get_reference_image_path():
    path = config.BASE_DIR / config.REFERENCE_ICON_NAME
    return path if path.exists() else None

def verify_visual_match(full_screenshot, x, y, reference_path):
    ref_img = cv2.imread(str(reference_path))
    if ref_img is None: return 0.0
    # Dynamic crop above text
    crop = cv2.resize(full_screenshot, None, fx=2, fy=2)[y-150:y-10, x-60:x+60]
    if crop.shape[0] < ref_img.shape[0] or crop.shape[1] < ref_img.shape[1]: return 0.0 
    result = cv2.matchTemplate(crop, ref_img, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(result)[1]

def run_ocr_on_image(processed_img, target_text):
    try:
        data = pytesseract.image_to_data(processed_img, config='--psm 11', output_type=pytesseract.Output.DICT)
        candidates = []
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if len(text) < 3: continue
            if fuzz.partial_ratio(target_text.lower(), text.lower()) > config.MATCH_THRESHOLD:
                candidates.append({
                    'text': text, 'x_raw': data['left'][i], 'y_raw': data['top'][i],
                    'x': data['left'][i]//2, 'y': data['top'][i]//2, 'w': data['width'][i]//2, 'h': data['height'][i]//2
                })
        return candidates
    except: return []

def find_icon_coordinates(image_path, project_dir):
    original_img = cv2.imread(image_path)
    ref_path = get_reference_image_path()
    all_candidates = []
    
    for filter_img in _apply_filters(original_img):
        found = run_ocr_on_image(filter_img, config.TARGET_ICON_TEXT)
        for cand in found:
            cand['visual_score'] = verify_visual_match(original_img, cand['x_raw'], cand['y_raw'], ref_path) if ref_path else 0.0
        all_candidates.extend(found)
    
    if all_candidates:
        all_candidates.sort(key=lambda x: (-x['visual_score'], -fuzz.ratio(config.TARGET_ICON_TEXT, x['text'])))
        best = all_candidates[0]
        return (best['x'] + (best['w'] // 2), best['y'] + (best['h'] // 2) - config.ICON_VERTICAL_OFFSET)
    return None

def save_debug_image(image_path, coords, save_dir):
    img = cv2.imread(image_path)
    cv2.circle(img, coords, 10, (0, 0, 255), -1) 
    cv2.imwrite(str(save_dir / config.DEBUG_FILENAME), img)
