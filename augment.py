import cv2
import numpy as np
import os
import random
from glob import glob

# ===== CONFIG =====
INPUT_DIR = "images/output/minutes1"          # Folder with original images
OUTPUT_DIR = "images/augmented/minutes1"      # Folder to save augmented images

NUM_AUGMENTS = 5              # Number of augmentations per image

# Probability for each augmentation to be applied
PROB_ROTATE = 0.7
PROB_SHIFT = 0.5
PROB_PERSPECTIVE = 0.5
PROB_NOISE = 0.6
PROB_BLUR = 0.5
PROB_BRIGHT_CONTRAST = 0.7

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== AUGMENTATION FUNCTIONS =====
def random_rotation(image, max_angle=5):
    angle = random.uniform(-max_angle, max_angle)
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

def random_shift(image, max_shift=5):
    h, w = image.shape[:2]
    dx = random.randint(-max_shift, max_shift)
    dy = random.randint(-max_shift, max_shift)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

def random_perspective(image, max_warp=0.02):
    h, w = image.shape[:2]
    pts1 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    delta = max_warp * min(w,h)
    pts2 = pts1 + np.random.uniform(-delta, delta, pts1.shape).astype(np.float32)
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

def random_noise(image, intensity=10):
    noise = np.random.normal(0, intensity, image.shape).astype(np.uint8)
    return cv2.add(image, noise)

def random_blur(image):
    ksize = random.choice([1, 3])
    if ksize > 1:
        return cv2.GaussianBlur(image, (ksize, ksize), 0)
    return image

def random_brightness_contrast(image, brightness=30, contrast=30):
    beta = random.randint(-brightness, brightness)
    alpha = 1 + random.uniform(-contrast/100, contrast/100)
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# ===== AUGMENTATION PIPELINE =====
def augment_image_random(image):
    aug = image.copy()
    if random.random() < PROB_ROTATE:
        aug = random_rotation(aug)
    if random.random() < PROB_SHIFT:
        aug = random_shift(aug)
    if random.random() < PROB_PERSPECTIVE:
        aug = random_perspective(aug)
    if random.random() < PROB_NOISE:
        aug = random_noise(aug)
    if random.random() < PROB_BLUR:
        aug = random_blur(aug)
    if random.random() < PROB_BRIGHT_CONTRAST:
        aug = random_brightness_contrast(aug)
    return aug

# ===== MAIN LOOP =====
image_paths = glob(os.path.join(INPUT_DIR, "*.*"))
count = 0

for img_path in image_paths:
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    image = cv2.imread(img_path)

    for i in range(NUM_AUGMENTS):
        aug_image = augment_image_random(image)
        out_path = os.path.join(OUTPUT_DIR, f"{img_name}_aug{i+1}.png")
        cv2.imwrite(out_path, aug_image)
        count += 1

print(f"✅ Generated {count} augmented images in '{OUTPUT_DIR}'")