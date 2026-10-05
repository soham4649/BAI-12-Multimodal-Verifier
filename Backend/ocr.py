import easyocr
import cv2
import re

reader = easyocr.Reader(["en"], gpu=False)


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to read image.")
    h, w = image.shape[:2]
    max_dim = max(h, w)
    if max_dim > 600:
        scale = 600.0 / max_dim
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    elif max_dim < 300:
        scale = 2.0
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def extract_text(image_path):
    try:
        processed = preprocess_image(image_path)
        results = reader.readtext(processed, detail=1, paragraph=False, width_ths=0.5)
        detected, seen = [], set()
        for item in results:
            if len(item) < 3 or item[2] < 0.45:
                continue
            text = re.sub(r"\s+", " ", item[1]).strip()
            if len(text) < 2 or text.lower() in seen:
                continue
            seen.add(text.lower())
            detected.append((text, item[2]))
        detected.sort(key=lambda x: x[1], reverse=True)
        return " ".join(text for text, _ in detected).strip()
    except Exception as exc:
        print("OCR Error:", exc)
        return ""
