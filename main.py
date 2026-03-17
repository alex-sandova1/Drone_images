from PIL import Image
from analyze_color import *
from config import *
from stitch import *

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
    else:
        print("No images found in the directory.")

if __name__ == "__main__":
    main()