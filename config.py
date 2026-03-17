from pathlib import Path
import numpy as np
import cv2

IMAGES_DIR = Path(__file__).parent / "data"
VALID_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}

def clean_mask(mask, k=5):
    kernel = np.ones((k, k), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask