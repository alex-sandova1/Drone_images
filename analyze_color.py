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
    
    deep_green_high = np.array([35,80,25], dtype=np.uint8)
    deep_green_low = np.array([90,255,120], dtype=np.uint8)
    
    beige_low = np.array([15,20,100], dtype=np.uint8)
    beige_high = np.array([35,160,255], dtype=np.uint8)
    
    #creates masks
    green = cv2.inRange(hsv, green_low, green_high)
    deep_green = cv2.inRange(hsv, deep_green_low, deep_green_high)
    beige = cv2.inRange(hsv, beige_low, beige_high)
    
    return green, deep_green, beige

