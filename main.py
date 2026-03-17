from PIL import Image
import cv2
import numpy as np

from analyze_color import clean_mask, pct
from config import IMAGES_DIR
from stitch import get_first_image

def main():
    print(f"Searching in: {IMAGES_DIR}")
    image_file = get_first_image()

    if image_file:
        with Image.open(image_file) as image:
            print(f"Image: {image_file.name}")
            print(f"Path: {image_file}")
            print(f"Format: {image.format}")
            print(f"Size: {image.size}")
            print(f"Mode: {image.mode}")

        # Testing clean_mask + pct on a simple threshold mask
        print("Reached mask test block")
        bgr = cv2.imread(str(image_file))
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        _, raw_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

        cleaned = clean_mask(raw_mask, k=5)

        print(f"Raw mask coverage: {pct(raw_mask):.2f}%")
        print(f"Cleaned mask coverage: {pct(cleaned):.2f}%")
    else:
        print("No images found in the directory.")

if __name__ == "__main__":
    main()