import os
import json
from glob import glob
from PIL import Image
import pytesseract
import re

# ===== CONFIG =====
INPUT_FOLDER = "images/augmented/minutes1"   # folder containing augmented images
OUTPUT_JSON = "jsons/minutes1.json"
LABEL = "minutes"                             # explicit label for this doc type

# Optional: tesseract config
TESSERACT_CONFIG = "--oem 3 --psm 4"

# ===== Cleaning Function =====
import re

import re

def clean_ocr_text(text):
    """
    Aggressively clean OCR text for any document type while preserving
    meaningful words, numbers, dates, grades, and key phrases.
    """

    # Normalize whitespace
    text = " ".join(text.split())

    # Remove repeated symbols (e.g., ----====, X-X-X-X)
    text = re.sub(r'([^\w\s])(?:\1[-\1]*){3,}', ' ', text)

    # Remove sequences of symbols that are likely garbage (≥5 chars)
    text = re.sub(r'\b[^\w\s]{5,}\b', ' ', text)

    # Remove very short nonsense tokens (1-2 chars of symbols only)
    text = re.sub(r'\b[^\w\s]{1,2}\b', ' ', text)

    # Remove stray punctuation surrounded by whitespace (like " , " or " ; ")
    text = re.sub(r'\s[^\w\s]\s', ' ', text)

    # Remove multiple consecutive non-alphanumeric symbols inside words
    text = re.sub(r'(?<=\w)[^\w\s]{2,}(?=\w)', '', text)

    # Remove stray non-printable/control characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    # Final cleanup: collapse multiple spaces
    text = " ".join(text.split())

    return text

# ===== OCR Loop =====
dataset = []

image_paths = glob(os.path.join(INPUT_FOLDER, "*.*"))
print(f"Processing {len(image_paths)} images for document type '{LABEL}'")

for img_path in image_paths:
    img_name = os.path.basename(img_path)
    print(f"  OCR: {img_name}")

    img = Image.open(img_path).convert("L")  # grayscale for better OCR
    ocr_text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)

    # Clean the OCR text
    ocr_text = clean_ocr_text(ocr_text)

    dataset.append({
        "image": img_name,
        "label": LABEL,
        "ocr_text": ocr_text
    })

# Save JSON
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(dataset)} samples to {OUTPUT_JSON}")