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


def make_color_mask(bgr):   #creates masks for green, deep green, and beige
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)  #turns image to HSV for easier color segmentation
    
    #Defines color parameters
    green_low = np.array([35,40,40], dtype=np.uint8)
    green_high = np.array([90,255,255], dtype=np.uint8)
    
    deep_green_low = np.array([35,80,25], dtype=np.uint8)
    deep_green_high = np.array([90,255,120], dtype=np.uint8)
    
    beige_low = np.array([15,20,100], dtype=np.uint8)
    beige_high = np.array([35,160,255], dtype=np.uint8)
    
    #creates masks
    green = cv2.inRange(hsv, green_low, green_high)
    deep_green = cv2.inRange(hsv, deep_green_low, deep_green_high)
    beige = cv2.inRange(hsv, beige_low, beige_high)
    
    return green, deep_green, beige


def analyze_land_cover(bgr, k=5):   #pipeline function 
    if bgr is None or bgr.size == 0:
        raise ValueError("Input image is empty or could not be read.")

    green, deep_green, beige = make_color_mask(bgr)
    green = clean_mask(green, k=k)
    deep_green = clean_mask(deep_green, k=k)
    beige = clean_mask(beige, k=k)
    
    return {
        "green": pct(green),
        "deep_green": pct(deep_green),
        "beige": pct(beige)
    }


def analyze_image_file(image_path, k=5):
    image_path = Path(image_path)
    bgr = cv2.imread(str(image_path))

    if bgr is None:
        raise ValueError(f"Unable to read image file: {image_path}")

    return analyze_land_cover(bgr, k=k)


def analyze_image_batch(image_paths, k=5):
    results = []

    for image_path in image_paths:
        image_path = Path(image_path)
        coverage = analyze_image_file(image_path, k=k)
        results.append({
            "image_path": image_path,
            **coverage,
        })

    return results

