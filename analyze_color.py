from pathlib import Path
import numpy as np
import cv2

def clean_mask(mask, k=5):
    kernel = np.ones((k, k), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

def pct(mask):
    return 100.0 * np.count_nonzero(mask) / mask.size